
class YandexWebhook:
	def __init__(self, json_obj):
		self._meta = json_obj.get('meta', {})
		self._session = json_obj.get('session', {})
		self._request = json_obj.get('request', {})
		self._version = json_obj.get('version', {})

	@property
	def token(self):
		return self._request.get('nlu', {}).get('token', [])

	@property
	def command(self):
		return self._request.get('command', None)

	@property
	def session_id(self):
		return self._session.get('session_id', None)

	def build_response(self, answer):
		return {
			'version': self._version,
			'session': self._session,
			'response': {
				'text': answer,
				'end_session': True
			}
		}


if __name__ == '__main__':
	resp = {
		"meta": {
			"locale": "ru-RU",
			"timezone": "UTC",
			"client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
			"interfaces": {
				"screen": {

				},
				"payments": {

				},
				"account_linking": {

				}
			}
		},
		"session": {
			"message_id": 0,
			"session_id": "",
			"skill_id": "",
			"user": {
				"user_id": ""
			},
			"application": {
				"application_id": ""
			},
			"user_id": "",
			"new": True
		},
		"request": {
			"command": "включи наруто",
			"original_utterance": "включи наруто",
			"nlu": {
				"tokens": [
					"включи",
					"наруто"
				],
				"entities": [
					{
						"type": "YANDEX.FIO",
						"tokens": {
							"start": 1,
							"end": 2
						},
						"value": {
							"first_name": "наруто"
						}
					}
				],
				"intents": {

				}
			},
			"markup": {
				"dangerous_context": False
			},
			"type": "SimpleUtterance"
		},
		"version": "1.0"
	}

	yw = YandexWebhook(resp)
	print(yw.command)
