import helpers
from plugins import mal

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
						  ConversationHandler)

from tg_commands import authorization
from tg_commands.control_cast import control_keyboard
from tg_commands.base.tg_mal import BaseTgMal


class UpdateEpisode(BaseTgMal):
	def __init__(self):
		super().__init__()
		self._current_watching = []

		self._choose_episode = 0

	@staticmethod
	def cancel(update, context):
		update.message.reply_text('отмена')
		return ConversationHandler.END

	@authorization.check_access
	def providing_info(self, update, context):
		# тут обновляется _current_watching
		super().provide_names(update, context)

		return self._choose_episode

	def choosing_episode(self, update, context):
		answer = update.message.text

		watching = helpers.objs_by_key(self._current_watching, 'name')

		choosed_anime = watching[answer]
		mal.update(
			choosed_anime['anime_id'],
			choosed_anime['num_watched_episodes'] + 1
		)
		update.message.reply_text(
			'Добавила одну серию',
			reply_markup=ReplyKeyboardMarkup(control_keyboard(), one_time_keyboard=False),
			parse_mode='Markdown'
		)
		return ConversationHandler.END

	def get_conversation_handler(self, cmd='update_ep'):
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
