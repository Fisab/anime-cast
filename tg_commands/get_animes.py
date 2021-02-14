import helpers

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
						  ConversationHandler)

from plugins import mal

from tg_commands import authorization
from tg_commands.control_cast import control_keyboard
from tg_commands.base.tg_mal import BaseTgMal


class GetAnimes(BaseTgMal):
	def __init__(self, cast, site):
		super().__init__()
		# make steps:
		self._provide_info, self._choose_episode = range(2)
		self._current_watching = []

		self.site = site
		self.cast = cast

	@authorization.check_access
	def providing_info(self, update, context):
		super().provide_names(update, context)

		return self._choose_episode

	def start_cast(self, choosed_anime):
		episode = choosed_anime['num_watched_episodes'] + 1
		anime_info = mal.describe_anime(choosed_anime['anime_id'])

		anime_video = self.site.search(
			keyword=choosed_anime['name'],
			need_year=anime_info['year'],
			episode=episode
		)
		if anime_video is None:
			return False
		return self.cast.cast(anime_video['url'])

	def choosing_episode(self, update, context):
		answer = update.message.text

		watching = helpers.objs_by_key(self._current_watching, 'name')

		choosed_anime = watching[answer]
		result = self.start_cast(choosed_anime)

		message = {
			True: 'Запускаю касету',
			False: 'Касетник сломался, попробуйте /change_chromecast\nНу или на сайте нету этой анимки... :('
		}.get(result)

		update.message.reply_text(
			message,
			reply_markup=ReplyKeyboardMarkup(control_keyboard(), one_time_keyboard=False),
		)

		return ConversationHandler.END

	@staticmethod
	def cancel(update, context):
		update.message.reply_text('отмена')
		return ConversationHandler.END

	def get_conversation_handler(self, cmd='get_animes'):
		return ConversationHandler(
			entry_points=[CommandHandler(cmd, self.providing_info)],

			states={
				self._choose_episode: [
					MessageHandler(Filters.text, self.choosing_episode),
					CommandHandler('cancel', self.cancel)
				],
			},

			fallbacks=[CommandHandler('cancel', self.cancel)]
		)
