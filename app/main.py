from flask import Flask, request, jsonify
from config import Config

from yandex_webhook import YandexWebhook
from alice_handler import AliceHandler

app = Flask(__name__)

config = Config()

via_webhook = True

if via_webhook is False:
	# для телеграм бота
	from bot import TelegramBot

	telegram_bot = TelegramBot(token=config.telegtam_token, via_polling=True)
	telegram_dispatcher = telegram_bot.get_dispatcher()
else:
	# для вебхуков Алисы
	from plugins import animego
	from plugins import mal
	from cast import Cast
	from mal2alice import Mal2Alice
	import time
	site = animego.Site()
	print('Caching mal...')
	mal2alice = Mal2Alice(mal, site)
	print('Finding chromecasts...')
	cast = Cast()


@app.route('/', methods=['GET'])
def index():
	return 'OK', 200

# не хочу пробрасывать вебхук со своим динамическим ip(
# @app.route('/webhook', methods=['GET', 'POST'])
# def pass_update():
# 	update = Update.de_json(request.get_json(force=True), telegram_bot)
# 	telegram_dispatcher.process_update(update)
# 	return 'OK'


def check_user_id(method):
	def check_headers(*args):
		if request.get_json().get('session', {}).get('user_id') == config.alice_uid:
			return method(*args)
		return 'go away', 200

	return check_headers


@app.route('/alice_webhook', methods=['POST'])
# @check_user_id
def anime():
	request_data = YandexWebhook(request.get_json())
	handler = AliceHandler(request_data, mal2alice, site, cast)

	return jsonify(handler.handle_request())


if __name__ == '__main__':
	if via_webhook is True:
		app.run(debug=True, host='0.0.0.0', port=322)
