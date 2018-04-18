import requests
from lxml import html
import json

config = json.load(open('data.json'))

def get_link_from_shik(url):
	new_url = get_voices_shik(url)
	if new_url == False:
		#bad link to shikimori or u havent favorite voice
		page = requests.get(url)
	else:
		page = requests.get(new_url)

	tree = html.fromstring(page.text)
	video = tree.xpath('//iframe')
	if len(video) > 0:
		video = video[0]
		video_src = video.attrib['src']
	
		return video_src
	else:
		return False

def get_voices_shik(url):#now support only dub
	page = requests.get(url)
	tree = html.fromstring(page.text)

	t = tree.xpath("//span[@class='video-author']")
	for i in t:#find all dubs
		for j in config['love_voices']:#find need voices
			if i.text.find(j) != -1:
				parent = i.getparent()#get parrent of voice(tag a)
				children = parent.getchildren()#children of need voice
				if children[0].text == 'Озвучка' and children[1].text == 'vk.com':#check is it vk and dub
					return parent.get('href')

	return False


