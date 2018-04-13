import pychromecast
import time

cast = None
mc = None

def init():
	global cast
	global mc

	chromecasts = pychromecast.get_chromecasts()
	if len(chromecasts) > 0:
		cast = chromecasts[0]
		mc = cast.media_controller
		return True
	return False

def cast(link):
	if mc == None:
		res = init()

	mc.play_media(link, 'video/mp4')
	mc.block_until_active()


def pause():
	if mc == None:
		res = init()

	mc.pause()

def play():
	if mc == None:
		res = init()

	mc.play()

def stop():
	if mc == None:
		res = init()
	mc.stop()