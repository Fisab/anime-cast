import json


class Config:
	def __init__(self):
		self.__config = json.load(open('data.json'))

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


if __name__ == '__main__':
	c = Config()
	print(c.mal_auth)