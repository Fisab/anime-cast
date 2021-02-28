import time
import helpers
from utils.stemming import Stemmer


class Mal2Alice:
	def __init__(self, mal, site, threshold=5 * 60 * 60):
		self._site = site
		self._mal = mal
		self._stemmer = Stemmer()

		self.animes = self._mal.get_all_translated_animes(site)
		print(self.animes)
		self._update_time = time.time()

		self.time_threshold = threshold

	def __update_if_need(self):
		if time.time() - self._update_time > self.time_threshold:  # прошло слишком много времени и надо обновить список
			print('Updating anime list...')
			self.animes = self._mal.get_all_translated_animes(self._site)
			self._update_time = time.time()

	def get_top_n_animes_names(self, n=5):
		return [anime['ru_title'] for anime in self.animes[:n]]

	def get_anime_by_id(self, anime_id):
		self.__update_if_need()
		return helpers.objs_by_key(self.animes, 'anime_id')[anime_id]

	def update_episode(self, anime_id):
		index = self.animes.index(self.get_anime_by_id(anime_id))
		self.animes[index]['num_watched_episodes'] += 1
		print('update mal', anime_id, self.animes[index]['num_watched_episodes'])
		status = self._mal.update(anime_id, self.animes[index]['num_watched_episodes'])
		return status

	def find_anime_name(self, keywords):
		"""
		:param keywords: по каким-то словам пытается найти максимально похожее аниме
		:return:
		"""
		keywords = [keywords] if isinstance(keywords, str) else keywords
		get_intersection = lambda a, b: list(set(a) & set(b))

		keywords = [self._stemmer.stem(keyword) for keyword in keywords if len(keyword) > 1]
		result = []

		for anime in self.animes:
			if anime['ru_title'] is None:
				continue

			title = [self._stemmer.stem(word) for word in anime['ru_title'].lower().split(' ') if len(word) > 1]
			result.append({
				'site_anime_id': anime['site_anime_id'],
				'title': anime['ru_title'],
				'name': anime['name'],
				'intersection': get_intersection(title, keywords),
				'stems': title,
				'anime_id': anime['anime_id'],
				'num_watched_episodes': anime['num_watched_episodes'],
				'published_episodes': anime['published_episodes'],
				'year': anime['year']
			})

		best_match = sorted(result, key=lambda x: len(x['intersection']))[::-1][0]
		if len(best_match['intersection']) > 0:
			return {
				'site_anime_id': best_match['site_anime_id'],
				'name': best_match['name'],
				'anime_id': best_match['anime_id'],
				'num_watched_episodes': best_match['num_watched_episodes'],
				'published_episodes': best_match['published_episodes'],
				'year': best_match['year']
			}


if __name__ == '__main__':
	from plugins import mal, animego

	site = animego.Site()

	mal2alice = Mal2Alice(mal, site)
	# mal2alice.update_episode(20)
	# print(mal2alice.get_anime_by_id(20))
	print(mal2alice.find_anime_name('пять'))
