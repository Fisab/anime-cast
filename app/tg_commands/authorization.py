from config import Config

config = Config()

ACCESS_LIST = config.telegram_access_list


def check_access(func_command):
	def accessed_func_command(*args):
		# deal with self
		if len(args) == 2:
			update, context = args
		else:
			_, update, context = args
		messages_uid = update['message']['chat']['id']

		if messages_uid in ACCESS_LIST:
			return func_command(*args)
		else:
			access_denied(update, context)
	return accessed_func_command


def access_denied(update, context):
	update.message.reply_text('пiшов нахуй', parse_mode='HTML')
