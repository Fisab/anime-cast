import requests
from lxml import html
import json


class Site:
	def __init__(self):
		self._base = 'https://animego.org'
		self.headers = json.load(open('plugins/headers.json'))

	@staticmethod
	def get_keys(obj, keys):
		return {k: v for k, v in obj.items() if k in keys}

	def get_kodif_info(self, kodik_link):
		splitted = kodik_link.split('/')
		data = {
			'hash2': 'vbWENyTwIn8I',
			'type': 'seria',
			'hash': splitted[5],
			'id': splitted[4]
		}
		resp = requests.post(
			'https://kodik.info/get-video-info',
			headers=self.headers,
			data=data
		)
		links = resp.json()['links']
		max_resolution = max([int(i) for i in links.keys()])
		return links[str(max_resolution)][0]['src'].replace(':hls:manifest.m3u8', '')

	def get_link(self, anime_id, episode):
		# выдираем из этой дрисни внутренний айдишник animego
		url = f'{self._base}/anime/{anime_id}/player?_allow=true'
		headers = {
			**self.headers,
			'x-requested-with': 'XMLHttpRequest'
		}

		resp = requests.get(url, headers=headers).json()
		tree = html.fromstring(resp['content'])
		childrens = tree.xpath('//*[@id="video-carousel"]')[0].getchildren()

		data_id = None
		for child in childrens:
			some_episode = child.getchildren()[0].attrib
			if int(some_episode['data-episode']) == episode:
				data_id = some_episode['data-id']

		# теперь сия чуда надо узнать внутренний айдишник хостинга...
		params = (
			# ('dubbing', '9'),
			# ('provider', '19'),
			('episode', episode),
			('id', data_id),
		)
		resp = requests.get(
			'https://animego.org/anime/series',
			headers=headers,
			params=params
		).json()
		tree = html.fromstring(resp['content'])
		players_xpath = '//*[@id="video-players"]/span'

		players = [span.attrib['data-player'] for span in tree.xpath(players_xpath)]

		# поддержка плеера ток kodik.info
		kodik_link = [player for player in players if player.find('kodik.info') != -1]

		if len(kodik_link) == 0:
			return
		return self.get_kodif_info(kodik_link[0])

	def search(self, keyword, need_year, episode):
		url = f'{self._base}/search/all?q={keyword}'
		page = requests.get(url)
		xpath_anime_block = '//div[@class="animes-grid-item-body card-body px-0"]'

		tree = html.fromstring(page.text)

		blocks = tree.xpath(xpath_anime_block)

		for block in blocks:
			try:
				year = block.xpath('.//span[@class="anime-year"]')[0].text_content()
			except:
				# там в конце идут уже не ссылки на аниме, а на людей
				return
			attribs = block.getchildren()[1].xpath('.//a')[0].attrib
			attribs['id'] = attribs['href'].split('-')[-1]
			if need_year == int(year):
				attribs['url'] = self.get_link(attribs['id'], episode)
				return attribs


if __name__ == '__main__':
	site = Site()
	result = site.search('naruto', 2002, 31)
	print(result)
	# {'href': 'https://animego.org/anime/naruto-102', 'title': 'Наруто', 'id': '102', 'url': 'https://cloud.kodik-cdn.com/animetvseries/b4f6777c19529f5f6b5da082fafa608086c1090a/c68474974bdc9f04ef703826c4e64773:2021021406/480.mp4'}
	# url = site.get_link(102, episode=30)
	# print(url)
