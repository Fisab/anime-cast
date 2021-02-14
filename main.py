from flask import Flask, request, jsonify
from telegram.update import Update
from bot import TelegramBot
from config import Config

app = Flask(__name__)

config = Config()
telegram_bot = TelegramBot(token=config.telegtam_token, via_polling=True)
telegram_dispatcher = telegram_bot.get_dispatcher()


# @app.route('/', methods=['GET'])
# def index():
# 	return 'OK', 200

# не хочу пробрасывать вебхук со своим динамическим ip(
# @app.route('/webhook', methods=['GET', 'POST'])
# def pass_update():
# 	update = Update.de_json(request.get_json(force=True), telegram_bot)
# 	telegram_dispatcher.process_update(update)
# 	return 'OK'


if __name__ == '__main__':
	# app.run(debug=True)
	pass
