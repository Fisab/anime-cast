import requests
from lxml import html

def get_link_from_shik(url):
	page = requests.get(url)

	tree = html.fromstring(page.text)
	video = tree.xpath('//iframe')[0]
	video_src = video.attrib['src']
	
	return video_src

