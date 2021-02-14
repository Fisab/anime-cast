from tg_commands import authorization

BASE_CMD_NAME = 'help'


@authorization.check_access
def send_help_msg(update, context):
	help_message = '''
	Дратути
	- /get_animes
	- /change_chromecast
	- /update_ep
	'''.strip()
	update.message.reply_text(help_message, parse_mode='HTML')
