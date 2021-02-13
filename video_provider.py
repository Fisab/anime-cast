from plugins import yummyanime


class VideoProvider:
	def __init__(self, site_anime):
		self.site_anime = site_anime
		# pass

	def get_video(self, mal_id):



if __name__ == '__main__':
	site = yummyanime.Site()

	getter = VideoProvider(site)

