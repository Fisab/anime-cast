import telebot
import json
import mal
import time

import get_video
import shik
import cast

config = json.load(open('data.json'))

token = config['tg']

bot = telebot.TeleBot(token)

usernames = ['fisab']

data = []

@bot.message_handler(commands=['help'])
def help(message):
	if not message.chat.username in usernames:
		bot.send_message(message.chat.id, 'пішов нахуй')
		return
	msg = 'Я умею делать следующие вещи:\n/get_animes - получить текущие анимки со статусом watching\n/pause - пауза\n/play - воспроизвести\n/update_ep - обновить кол-во просмотренных эпизодов'

	bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['get_animes'])
def get_animes(message):
	if not message.chat.username in usernames:
		bot.send_message(message.chat.id, 'пішов нахуй')
		return
	global data
	animes = mal.get_current_watching()
	data = []
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
		msg += 'id - ' + str(len(data)-1) + '; ' + i['anime_title'] + ' ' + str(i['num_watched_episodes']) + '/' + str(i['anime_num_episodes']) + '\n'# + i['anime_image_path'] + '\n' image if need
		# bot.send_message(message.chat.id, msg)
	bot.send_message(message.chat.id, msg)

	sent = bot.send_message(message.chat.id, 'Выберите номер аниме. -1 - отмена')
	bot.register_next_step_handler(sent, choose_episode)

def choose_episode(message):
	if int(message.text) != -1:
		choosed_anime = data[int(message.text)]


		episode = choosed_anime['num_watched_episodes'] + 1
		url = 'https://play.shikimori.org/animes/' + str(choosed_anime['anime_id']) + '/video_online/' + str(episode)

		video_src = shik.get_link_from_shik(url)#vk
		link = get_video.get_link(video_src)

		result = cast.cast(link)

		if result == True:
			cast_now = True
			bot.send_message(message.chat.id, 'Трансляция вот-вот начнется, для паузы отправьте /pause , для отмены - /stop')
		else:
			bot.send_message(message.chat.id, 'Малинке не удалось найти chromecast, проверьте включен ли он.')

@bot.message_handler(commands=['pause'])
def set_pause(message):
	if not message.chat.username in usernames:
		bot.send_message(message.chat.id, 'пішов нахуй')
		return
	cast.pause()
	bot.send_message(message.chat.id, 'Поставила на паузу')

@bot.message_handler(commands=['play'])
def set_pause(message):
	if not message.chat.username in usernames:
		bot.send_message(message.chat.id, 'пішов нахуй')
		return
	cast.play()
	bot.send_message(message.chat.id, 'Поставила воспроизводить')

@bot.message_handler(commands=['update_ep'])
def update_anime(message):
	sent = bot.send_message(message.chat.id, 'Введи id анимки')
	bot.register_next_step_handler(sent, choose_episode)

def update_anime1(message):
	choosed_anime = data[int(message.text)]
	mal.update_anime(choosed_anime['anime_id'], choosed_anime['num_watched_episodes'] + 1)

while True:
	try:
		bot.polling(none_stop=True)
	except:
		time.sleep(10)
