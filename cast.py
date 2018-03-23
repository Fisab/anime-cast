import pychromecast
import time

cast = None
mc = None

def cast(link):
	global cast
	global mc

	chromecasts = pychromecast.get_chromecasts()
	if len(chromecasts) > 0:
		cast = chromecasts[0]
		mc = cast.media_controller
		mc.play_media(video, 'video/mp4')
		mc.block_until_active()

		return True
	return False

def pause():
	mc.pause()

def play():
	mc.play()