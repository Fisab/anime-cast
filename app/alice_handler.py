

class AliceHandler:
	def __init__(self, yandex_webhook, mal2alice, site, cast):
		self._yandex_webhook = yandex_webhook
		self._mal2alice = mal2alice
		self._site = site
		self._cast = cast

		self.cmd_play_ = ['включи', 'включай', 'включить']
		self.cmd_play_next = ['следующую', 'следующий', 'следующая', 'следующий']

		self.notice_mal = ['отметь', 'отмечай', 'пометь', 'отметить']

		self.get_watching = ['какое', 'аниме', 'смотрю']

		self.pause = ['пауза', 'останови', 'паузу']
		self.play = ['запусти', 'воспроизведи', 'воспроизвести']
		self.forward = ['вперед']
		self.back = ['назад']
		self.stop = ['стоп']

		self.where_is = ['сколько', 'посмотрел', 'вышло']

		# statuses
		self.__idk = 'че за хуйню ты подсунул'
		self.__done = 'дыа'
		self.__failed = 'чет не получилось'

	@staticmethod
	def _iter_find(text, keywords):
		return bool(sum(text.find(keyword) != -1 for keyword in keywords))

	@staticmethod
	def handle_nonexistent():
		return 'отстань'

	def process_notice(self, message):
		anime = self._mal2alice.find_anime_name(message.split(' '))
		if anime is None:
			return self.__idk
		status = self._mal2alice.update_episode(anime['anime_id'])
		if status is True:
			return 'готово'
		return self.__failed

	def process_play(self, message, next):
		anime = self._mal2alice.find_anime_name(message.split(' '))
		if anime is None:
			return self.__idk
		if next is True:
			self._mal2alice.update_episode(anime['anime_id'])
		cast_link = self._site.get_link(anime['site_anime_id'], anime['num_watched_episodes'] + 1)
		self._cast.cast(cast_link)
		return 'поставила касету'
		# return str(anime)
		# self._mal2alice

	def get_where_is(self, message):
		anime = self._mal2alice.find_anime_name(message.split(' '))
		if anime is None:
			return self.__idk
		print(anime)
		return f"ты посмотрел {anime['num_watched_episodes']} из {anime['published_episodes']} вышедших"

	def detect_command(self, message):
		print('Получил: ', message)
		# включить аниме
		if self._iter_find(message, self.cmd_play_):
			# включить следующую серию (чтобы не отмечать лишней командой)
			next = self._iter_find(message, self.cmd_play_next)
			return self.process_play(message, next)

		# отметить аниме
		elif self._iter_find(message, self.notice_mal):
			return self.process_notice(message)

		# что я смотрю
		elif self._iter_find(message, self.get_watching):
			return '\n'.join(self._mal2alice.get_top_n_animes_names())

		# перемотать вперед
		elif self._iter_find(message, self.forward):
			self._cast.seek(90)
			return self.__done

		# перемотать назад
		elif self._iter_find(message, self.back):
			self._cast.seek(-90)
			return self.__done

		# пауза
		elif self._iter_find(message, self.pause):
			self._cast.pause()
			return self.__done

		# воспроизведи
		elif self._iter_find(message, self.play):
			self._cast.play()
			return self.__done

		# стоп
		elif self._iter_find(message, self.stop):
			self._cast.stop()
			return self.__done

		# сколько вышло серий (онгоинги)...
		elif self._iter_find(message, self.where_is):
			return self.get_where_is(message)

		else:
			return self.handle_nonexistent()

	def handle_request(self):
		answer = self.detect_command(self._yandex_webhook.command)
		return self._yandex_webhook.build_response(answer)
