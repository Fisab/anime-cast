import requests
import json
from lxml import html
import config

config_obj = config.Config()
BASE = 'https://myanimelist.net'


def get_current_watching():
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
		'status': 2,
		# 'score': 0,
		'num_watched_episodes': episode,
		'csrf_token': config_obj.mal_token
	}
	headers = {
		'cookie': config_obj.mal_cookie,
	}


	r = requests.post(
		'https://myanimelist.net/ownlist/anime/edit.json',
		data=json.dumps(data),
		headers=headers
	)
	print(r.status_code)

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


if __name__ == '__main__':
	update(20, 30)
	# a = get_current_watching()
	# print(a)
	# desc = describe_anime(20)
	# print(desc)

# print(tuple(config_obj.mal_auth.values()))
