import requests
import json
from lxml import html

config = json.load(open('data.json'))

def get_current_watching():
	url = 'https://myanimelist.net/animelist/%s/load.json?offset=0&status=1' % config['login']#current watching

	r = requests.get(url)
	data = r.json()
	return data


def get_img(link):#high quality
	url = 'https://myanimelist.net' + link
	page = requests.get(url)
	tree = html.fromstring(page.text)
	img = tree.xpath('//img[@class="ac"]')[0]
	return img.attrib['src']

# animes = get_current_watching()
# print(animes[0])
# for i in animes:
# 	print(get_img(i['anime_url']))


def update(status, episode, id):
	data = [
		('data', '<entry><status>%s</status><episode>%s</episode></entry>' % (status, episode)),
	]

	response = requests.post('https://myanimelist.net/api/animelist/update/%s.xml' % id, data=data, auth=(config['login'], config['password']))

def update_anime(id, num_ep):
	update(1, num_ep, id)

def drop_anime(id, num_ep):
	update(4, num_ep, id)

def complete_anime(id, num_ep):
	update(2, num_ep, id)


if __name__ == '__main__':
	update_anime(22199, 2)