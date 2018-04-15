import pychromecast
import time

class Cast:
	def init(self):
		chromecasts = pychromecast.get_chromecasts()
		if len(chromecasts) > 0:
			self.cast_ = chromecasts[0]
			self.mc = self.cast_.media_controller
			return True
		print('Get something troubles with find chromecast')
		return False

	def __init__(self):
		self.watching = False
		self.ready = False

		res = self.init()
		if res == True:
			self.ready = True

	def cast(self, link):
		if self.ready == True:
			self.mc.play_media(link, 'video/mp4')
			self.mc.block_until_active()

			self.watching = True

			return True
		return False

	def pause(self):
		if self.ready == True:
			self.mc.pause()
			return True
		return False

	def play(self):
		if self.ready == True:
			self.mc.play()
			return True
		return False

	def stop(self):
		if self.ready == True:
			self.mc.stop()
			self.watching = False
			return True
		return False

	def seek(self, ts):
		if self.ready == True:
			cur_time = self.mc.status.current_time
			new_time = cur_time + ts
			self.mc.seek(new_time)
			return True
		return False