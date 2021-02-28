import helpers

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
						  ConversationHandler)


def control_keyboard():
	return [
		['/stop', '/play', '/pause'],
		['/back', '/forw'],
		['/update_ep', '/get_animes']
	]


class ControlCast:
	def __init__(self, cast):
		self._cast = cast

		self._choose_chromecast = 0

	def forward(self, update, context):
		self._cast.seek(90)

		update.message.reply_text(
			'Кручу касету вперед',
			reply_markup=ReplyKeyboardMarkup(control_keyboard(), one_time_keyboard=False),
			parse_mode='Markdown'
		)

	def back(self, update, context):
		self._cast.seek(-90)

		update.message.reply_text(
			'Кручу касету назад',
			reply_markup=ReplyKeyboardMarkup(control_keyboard(), one_time_keyboard=False),
			parse_mode='Markdown'
		)

	def stop(self, update, context):
		self._cast.stop()

		update.message.reply_text(
			'Вытаскиваю касету',
			reply_markup=ReplyKeyboardMarkup(control_keyboard(), one_time_keyboard=False),
			parse_mode='Markdown'
		)

	def pause(self, update, context):
		self._cast.pause()

		update.message.reply_text(
			'Держу касету',
			reply_markup=ReplyKeyboardMarkup(control_keyboard(), one_time_keyboard=False),
			parse_mode='Markdown'
		)

	def play(self, update, context):
		self._cast.play()

		update.message.reply_text(
			'Отпускаю касету',
			reply_markup=ReplyKeyboardMarkup(control_keyboard(), one_time_keyboard=False),
			parse_mode='Markdown'
		)

	def reinit_chromecasts(self, update, context):
		found_chromecasts = self._cast.get_available_chromecasts()
		keyboard = helpers.split(found_chromecasts, 3)
		update.message.reply_text(
			'Выбирай',
			reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
			parse_mode='Markdown'
		)
		return self._choose_chromecast

	def choose_chromecast(self, update, context):
		answer = update.message.text

		result = self._cast.init(friendly_name=answer)

		message = {
			True: 'Переключила',
			False: 'Такой касетник не могу найти'
		}.get(result)

		update.message.reply_text(message)

		return ConversationHandler.END

	@staticmethod
	def cancel(update, context):
		update.message.reply_text('отмена')
		return ConversationHandler.END

	def get_conversation_handler(self, cmd='change_chromecast'):
		return ConversationHandler(
			entry_points=[CommandHandler(cmd, self.reinit_chromecasts)],

			states={
				self._choose_chromecast: [
					MessageHandler(Filters.text, self.choose_chromecast),
					CommandHandler('cancel', self.cancel)
				],
			},

			fallbacks=[CommandHandler('cancel', self.cancel)]
		)

