import tg_commands as commands

from cast import Cast
from plugins.animego import Site

from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

"""
All handler's functions must have '_handler' at the end for bot.py class add this handlers
"""
cast = Cast()
site = Site()  # скрапер видосов
cast_tg = commands.ControlCast(cast)


def help_handler(cmd='help'):
	return CommandHandler(cmd, commands.send_help_msg)


def get_animes_handler(cmd='get_animes'):
	return commands.GetAnimes(cast, site).get_conversation_handler(cmd)


def update_episode_handler(cmd='update_ep'):
	return commands.UpdateEpisode().get_conversation_handler(cmd)


def forward_handler(cmd=None):
	if cmd is None:
		cmd = ['forw', 'forward']
	return CommandHandler(cmd, cast_tg.forward)


def back_handler(cmd='back'):
	return CommandHandler(cmd, cast_tg.back)


def stop_handler(cmd='stop'):
	return CommandHandler(cmd, cast_tg.stop)


def pause_handler(cmd='pause'):
	return CommandHandler(cmd, cast_tg.pause)


def play_handler(cmd='play'):
	return CommandHandler(cmd, cast_tg.play)


def change_chromecast_handler(cmd='change_chromecast'):
	return cast_tg.get_conversation_handler(cmd)

