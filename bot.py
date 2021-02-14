import os
import logging

import telegram

from telegram.ext import Updater
import handler


class TelegramBot:
	def __init__(self, token=None, via_polling=False, use_proxy=False):
		self.token = token
		self.__bot = telegram.Bot(self.token)

		self.updater = self.setup_updater(use_proxy=use_proxy)
		self.__dispatcher = self.updater.dispatcher

		logging.basicConfig(
			format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
			level=logging.INFO
		)

		self.logger = logging.getLogger(__name__)

		self.setup_handlers()
		if via_polling is True:
			self.setup_polling()
		else:
			self.setup_webhook()

	def get_dispatcher(self):
		return self.__dispatcher

	def get_bot(self):
		return self.updater.bot

	def describe(self):
		return self.__bot.getMe()

	def send_message(self, recipient_id, message, parse_mode='HTML'):
		return self.__bot.sendMessage(chat_id=recipient_id, text=message, parse_mode=parse_mode)

	def error(self, context, update, error):
		"""Log Errors caused by Updates."""
		self.logger.warning('Update "%s" caused error "%s"', update, error)

	def setup_webhook(self, webhook_url):
		self.updater.start_webhook(listen='0.0.0.0', port=80, url_path='webhook')
		self.updater.bot.set_webhook(url=webhook_url)

	def setup_polling(self):
		self.updater.start_polling()

	def setup_handlers(self):
		for method_name in dir(handler):
			if method_name.endswith('_handler'):
				method = getattr(handler, method_name)
				self.__dispatcher.add_handler(method())
		self.__dispatcher.add_error_handler(self.error)

	def setup_updater(self, use_proxy=False):
		# когда-то это было нужно...
		if use_proxy is True:
			REQUEST_KWARGS = {
				'proxy_url': '',
				'urllib3_proxy_kwargs': {
					'username': '',
					'password': '',
				}
			}
			return Updater(self.token, request_kwargs=REQUEST_KWARGS)
		else:
			return Updater(self.token)
