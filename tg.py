import telebot
import json
import mal
import time

import get_video
import shik
import cast
import traceback

config = json.load(open('data.json'))

token = config['tg']

bot = telebot.TeleBot(token)

usernames = ['fisab']

data = []

cast_ = cast.Cast()

@bot.message_handler(commands=['help'])
def help(message):
	if not message.chat.username in usernames:
		bot.send_message(message.chat.id, 'пішов нахуй')
		return
	msg = 'Я умею делать следующие вещи:\n/get_animes - получить текущие анимки со статусом watching'

	bot.send_message(message.chat.id, msg)

def init_list():
	global data
	animes = mal.get_current_watching()
	data = []
	msg = ''
	for i in animes:
		# img = mal.get_img(i['anime_url']) high size img
		data.append({
			'anime_num_episodes': i['anime_num_episodes'],
			'num_watched_episodes': i['num_watched_episodes'],
			'url': i['anime_url'],
			'img': i['anime_image_path'],
			'name': i['anime_title'],
			'anime_id': i['anime_id']
		})
#
@bot.message_handler(commands=['get_animes'])
def get_animes(message):
	if not message.chat.username in usernames:
		bot.send_message(message.chat.id, 'пішов нахуй')
		return

	init_list()
	global data
	msg = ''
	for i in data:
		msg += 'id - ' + str(data.index(i)) + '; ' + i['name'] + ' ' + str(i['num_watched_episodes']) + '/' + str(i['anime_num_episodes']) + '\n'# + i['anime_image_path'] + '\n' image if need

	bot.send_message(message.chat.id, msg)

	sent = bot.send_message(message.chat.id, 'Выберите номер аниме. -1 - отмена')
	bot.register_next_step_handler(sent, choose_episode)
#
def choose_episode(message):
	if int(message.text) != -1:
		choosed_anime = data[int(message.text)]


		episode = choosed_anime['num_watched_episodes'] + 1
		url = 'https://play.shikimori.org/animes/' + str(choosed_anime['anime_id']) + '/video_online/' + str(episode)
		print('Try get through normal id')

		video_src = shik.get_link_from_shik(url)#vk

		if video_src == False:#some video starts zID idk all structure
			url = 'https://play.shikimori.org/animes/z' + str(choosed_anime['anime_id']) + '/video_online/' + str(episode)
			video_src = shik.get_link_from_shik(url)#vk
			print('Try get through z id')

		# print(video_src, url)
		link = get_video.get_link(video_src, choosed_anime['name'])
		print('link = %s' % link)
		result = cast_.cast(link)
		control_panel(message)

		if result == True:
			cast_now = True
			bot.send_message(message.chat.id, 'Трансляция вот-вот начнется, для паузы отправьте /pause , для отмены - /stop')
		else:
			bot.send_message(message.chat.id, 'Малинке не удалось найти chromecast, проверьте включен ли он.')

#
@bot.message_handler(commands=['pause'])
def set_pause(message):
	if not message.chat.username in usernames:
		bot.send_message(message.chat.id, 'пішов нахуй')
		return
	cast_.pause()
	bot.send_message(message.chat.id, 'Поставила на паузу')
#

@bot.message_handler(commands=['play'])
def set_pause(message):
	if not message.chat.username in usernames:
		bot.send_message(message.chat.id, 'пішов нахуй')
		return
	cast_.play()
	bot.send_message(message.chat.id, 'Поставила воспроизводить')

#
@bot.message_handler(commands=['update_ep'])
def update_anime(message):
	sent = bot.send_message(message.chat.id, 'Введи id анимки')
	bot.register_next_step_handler(sent, update_anime1)

def update_anime1(message):
	init_list()
	choosed_anime = data[int(message.text)]
	mal.update_anime(choosed_anime['anime_id'], choosed_anime['num_watched_episodes'] + 1)
	bot.send_message(message.chat.id, str(choosed_anime['anime_id']) + ' ты посмотрел столько эпизодов: ' + str(choosed_anime['num_watched_episodes']))
#

@bot.message_handler(commands=['stop'])
def stop(message):
	cast_.stop()
	bot.send_message(message.chat.id, 'Выключила')

#
@bot.message_handler(commands=['forw', 'forward'])
def rewind(message):
	cast_.seek(90)
	bot.send_message(message.chat.id, 'Перемотала вперед на 1 минуту')

@bot.message_handler(commands=['back'])
def rewind1(message):
	cast_.seek(-90)
	bot.send_message(message.chat.id, 'Перемотала назад на 1 минуту')
#

def control_panel(message):
	keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

	btn_stop = telebot.types.KeyboardButton(text='/stop')
	btn_play = telebot.types.KeyboardButton(text='/play')
	btn_pause = telebot.types.KeyboardButton(text='/pause')

	keyboard.add(btn_stop, btn_pause, btn_play)

	btn_forward = telebot.types.KeyboardButton(text='/forw')
	btn_back = telebot.types.KeyboardButton(text='/back')

	keyboard.add(btn_back, btn_forward)

	bot.send_message(message.chat.id, "Панель управления:", reply_markup=keyboard)

while True:
	try:
		bot.polling(none_stop=True)
	except:
		print(traceback.format_exc())
		time.sleep(10)


