from plugins import mal
import helpers
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)


class MalFetcher:
	def __init__(self):
		self._current_watching = []
		self.mal_prefix = 'https://myanimelist.net'

	def provide_names(self, update, context):
		self._current_watching = mal.get_current_watching()
		message = ''
		for some_anime in self._current_watching:
			message += f'[{some_anime["name"]}]({self.mal_prefix + some_anime["url"]}) - ' \
					   f'*{some_anime["num_watched_episodes"]}*/{some_anime["anime_num_episodes"]}\n'

		reply_keyboard = helpers.split([i['name'] for i in self._current_watching], n=2)

		update.message.reply_text(
			message,
			reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
			parse_mode='Markdown'
		)
