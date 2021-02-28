import json


class Config:
	def __init__(self):
		self.__config = json.load(open('../data.json'))

	@property
	def mal_auth(self):
		return self.__config['mal']

	@property
	def telegtam_token(self):
		return self.__config['telegram_token']

	@property
	def mal_token(self):
		return self.__config['mal_token']

	@property
	def mal_cookie(self):
		return self.__config['mal_cookie']

	@property
	def telegram_access_list(self):
		return self.__config['telegram_access_list']

	@property
	def alice_uid(self):
		return self.__config['alice_uid']


if __name__ == '__main__':
	c = Config()
	print(c.mal_auth)
