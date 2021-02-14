import pychromecast
import time
from pychromecast.controllers.youtube import YouTubeController


class Cast:
	def init(self, friendly_name='big room'):
		chromecasts, _ = pychromecast.get_chromecasts()
		chromecasts = [cc for cc in chromecasts if cc.device.model_name == 'Chromecast']
		if friendly_name is not None:
			chromecasts = [cc for cc in chromecasts if cc.device.friendly_name == friendly_name]
		if len(chromecasts) > 0:
			self.cast_ = chromecasts[0]
			self.mc = self.cast_.media_controller
			return True
		print('Get something troubles with find chromecast')
		return False

	def __init__(self):
		self.watching = False
		self.ready = False
		self.yt = None

		self.cast_ = None
		self.mc = None

		res = self.init()
		if res is True:
			self.ready = True

	@staticmethod
	def get_available_chromecasts():
		chromecasts, _ = pychromecast.get_chromecasts()
		return [cc.device.friendly_name for cc in chromecasts if cc.device.model_name == 'Chromecast']

	def cast(self, link):
		if self.ready is True:
			self.cast_.wait()
			self.mc.play_media(link, 'video/mp4')
			self.mc.block_until_active()
			self.watching = True

			return True
		return False

	def pause(self):
		if self.ready is True:
			self.mc.pause()
			return True
		return False

	def play(self):
		if self.ready is True:
			self.mc.play()
			return True
		return False

	def stop(self):
		if self.ready is True:
			self.mc.stop()
			self.watching = False
			return True
		return False

	def seek(self, ts):
		if self.ready is True:
			cur_time = self.mc.status.current_time
			new_time = cur_time + ts
			self.mc.seek(new_time)
			return True
		return False

	def cast_youtube(self, video_id):
		if self.yt is None:
			yt = YouTubeController()
			self.cast_.register_handler(yt)
		yt.play_video(video_id)
		return True


if __name__ == '__main__':
	c = Cast()
	print(c.get_available_chromecasts())
	# c.init()
	# print(c.ready)
	# c.cast('https://cloud.kodik-cdn.com/animetvseries/f5506632860aae587052161f800f1e990445d2f0/176a969a6978897de1a9f1f8f920ffe1:2021021405/480.mp4')
	# c.stop()
	# time.sleep(2)
	# c.pause()
	# time.sleep(2)
	# c.play()