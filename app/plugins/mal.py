import requests
import json
from lxml import html
from tqdm import tqdm

import sys
sys.path.insert(0, "..")
from helpers import retry
import config

config_obj = config.Config()
BASE = 'https://myanimelist.net'


def __get_current_watching():
	url = f'{BASE}/animelist/{config_obj.mal_auth["login"]}/load.json?offset=0&status=1'  # current watching

	r = requests.get(url)
	data = r.json()
	return data


def get_img(link):  # high quality
	url = f'{BASE}{link}'
	page = requests.get(url)
	tree = html.fromstring(page.text)
	img = tree.xpath('//img[@class="ac"]')[0]
	return img.attrib['src']


def update(id, episode):
	data = {
		'anime_id': id,
		'status': 1,  #2,
		# 'score': 0,
		'num_watched_episodes': episode,
		'csrf_token': config_obj.mal_token
	}
	headers = {
		'cookie': config_obj.mal_cookie
	}

	r = requests.post(
		'https://myanimelist.net/ownlist/anime/edit.json',
		data=json.dumps(data),
		headers=headers
	)
	# print(r.status_code)
	return r.status_code == 200

# def update(status, episode, id):
# 	data = [
# 		('data', f'<entry><status>{status}</status><episode>{episode}</episode></entry>'),
# 	]
#
# 	response = requests.post(f'{BASE}/api/animelist/update/{id}.xml', data=data,
# 							 auth=tuple(config_obj.mal_auth.values()))
# 	print(response.status_code)


# def update_anime(id, num_ep):
# 	update(1, num_ep, id)
#
#
# def drop_anime(id, num_ep):
# 	update(4, num_ep, id)
#
#
# def complete_anime(id, num_ep):
# 	update(2, num_ep, id)


@retry
def describe_anime(id):
	url = f'{BASE}/anime/{id}'

	build_xpath = lambda name: (f'//span[text()="{name}"]', name)

	attr_xpath = {
		'episodes': build_xpath('Episodes:'),
		'premiered': build_xpath('Premiered:')
	}

	page = requests.get(url)
	tree = html.fromstring(page.text)

	result = {
		key: tree.xpath(xpath[0])[0].getparent().text_content().replace(xpath[1], '').strip()
		for key, xpath in attr_xpath.items()
	}
	result['year'] = [int(s) for s in result['premiered'].split() if s.isdigit()][0]

	return result


def get_current_watching():
	current_watching = []

	animes = __get_current_watching()

	keys = {
		'High': 0,
		'Medium': 1,
		'Low': 2
	}
	# отсортируем по приоритету, чтобы вверху были самые приоритетные анимки
	for anime in sorted(animes, key=lambda x: keys.get(x['priority_string'])):
		# img = mal.get_img(i['anime_url']) high size img
		current_watching.append({
			'anime_num_episodes': anime['anime_num_episodes'],
			'num_watched_episodes': anime['num_watched_episodes'],
			'url': anime['anime_url'],
			'img': anime['anime_image_path'],
			'name': anime['anime_title'],
			'anime_id': anime['anime_id']
		})

	return current_watching


def translate_anime_name(anime_data, site):
	anime_info = describe_anime(anime_data['anime_id'])
	result = site.search(
		keyword=anime_data['name'],
		need_year=anime_info.get('year')
	)
	return {
		'ru_title': result.get('title'),
		'year': anime_info.get('year'),
		'site_anime_id': result.get('id'),
		'published_episodes': result.get('published_episodes')
	}


def get_all_translated_animes(site):
	animes = get_current_watching()
	return [{
		**anime,
		**translate_anime_name(anime, site)
	} for anime in tqdm(animes)]


if __name__ == '__main__':
	update(20, 99)
	# translate_anime_name(20)


	# a = get_current_watching()
	# print(a)
	# desc = describe_anime(20)
	# print(desc)

# print(tuple(config_obj.mal_auth.values()))
