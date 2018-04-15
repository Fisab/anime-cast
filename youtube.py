import json
from random import randint
import requests

videos = json.load(open('youtube.json'))

def get_rand_video():
	#for some videos need signature idk where get its and i just ignore this vides
	#i dont make it through pychromecast because there issue and it dont start play video(only show splash screen)
	r = [{'sp': 0}]
	while 'sp' in r[0]:
		id =  videos['love_videos'][randint(0, len(videos['love_videos'])-1)]
		url = 'https://you-link.herokuapp.com/?url=https://www.youtube.com/watch?v=' + id

		r = requests.get(url).json()
	# print(r[0]['url'])
	return r[0]['url']

if __name__ == '__main__':
	print(get_rand_video())