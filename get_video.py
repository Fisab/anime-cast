import requests
import json
import re

token = json.load(open('data.json'))['vk_token']

quality = [240, 360, 480, 720, 1080]

def get_vk_video_url(video_id):
	url = 'https://api.vk.com/method/video.get?videos={id}&access_token={token}&v=5.14'.format(id=video_id, token=token)
	r = requests.get(url)
	data = json.loads(r.text)['response']['items'][0]
	return data['player']

def get_vk_video(url, resolution):
	r = requests.get(url)

	#find resolutions
	av_res = re.findall(r'\.[0-9]{3,4}\.', r.text)
	for i in range(len(av_res)):
		av_res[i] = int(av_res[i].replace('.', ''))
	data = re.search(r'var playerParams =.*};', r.text).group().replace(';','').replace('var playerParams =','')
	data = json.loads(data)

	links = {}
	for i in quality:
		for j in data['params']:
			if 'url%i' % i in j:
				links[str(i)] = j['url%i' % i]

	if resolution == 'max':
	 	return links[max(links.keys())]

	elif str(resolution) in links.keys():
		return links[resolution]
		
	return None

def get_link(url, name_anime):
	if url.find('sovetromantica.com') != -1:
		anime_name = name_anime.lower().replace(' ', '-')
		numb_ep = url.split('_')[2].split('-')[0]
		anime_id = url.split('_')[1]
		link = 'https://chitoge.sovetromantica.com/anime/{name}/episodes/dubbed/episode_{ne}.mp4'.format(name=str(anime_id) + '_' + anime_name, ne=numb_ep)

		return link
	else:
		id = url.split('oid=')[1]
		id = id.split('&hash')[0]
		id = id.replace('&id=', '_')

		url = get_vk_video_url(id)
		link = get_vk_video(url, 'max')
		
		return link

# http://sovetromantica.com/embed/episode_438_13-dubbed

# https://chitoge.sovetromantica.com/anime/438_grancrest-senki/episodes/dubbed/episode_13.mp4