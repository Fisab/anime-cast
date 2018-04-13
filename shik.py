import requests
from lxml import html

def get_link_from_shik(url):
	page = requests.get(url)

	tree = html.fromstring(page.text)
	video = tree.xpath('//iframe')
	if len(video) > 0:
		video = video[0]
		video_src = video.attrib['src']
	
		return video_src
	else:
		return False

