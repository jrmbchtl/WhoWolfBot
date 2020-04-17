#!/usr/bin/python3

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, User
import requests
import re
import random
import time
import threading
import secrets
from telegram.error import Unauthorized
from telegram import ParseMode
import lore

token = ''
with open('token.txt', 'r') as token_file:
	token = token_file.readline()

print(token)

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

game_dict={}

game_library = {"single_player":False,
				"player_list":[],
				"anklage_list":[],
				"vote_list" : [],
				"werwolf_target_list" : [],
				"werwolf_target" : 0,
				"hexe_target" : 0,
				"admin_id" : 0,
				"game_chat_id" : 0,
				"running" : False,
				"round_number" : 0,
				"game_thread" : 0,
				"game_over_check" : False,
				"game_state" : None,
				"game_state_backup" : None,
				"hexe_life_juice_used" : False,
				"hexe_death_juice_used" : False,
				"vote_options" : {},
				"harter_bursche_survive" : True,
				"first_patt" : True,
				"werwolf_text" : {},
				"anklage_message_id": 0,
				"anklage_text" : {},
				"vote_message_id": 0,
				"vote_text" : {}}

werwolf_group = ["Werwolf", "Terrorwolf"]
dorf_group = ["Dorfbewohner", "Dorfbewohnerin", "Jäger", "Seherin", "Hexe", "Rotkäppchen", "HarterBursche", "Psychopath"]

markup_character = "`"
markup_character = "__"

class Target:
	def __init__(self, wolf_id, target_id):
		self.wolf_id = wolf_id
		self.target_id = target_id

class Spieler:
	def __init__(self, user_id, name):
		self.name = name
		self.user_id = user_id
		self.role = None
		self.werwolf_message_id = 0
		self.alive = True
		self.marked_by_werwolf = False
		self.marked_by_witch = False
		self.marked_by_psychopath = False

	def kill(self, context, game_id):
		self.alive = False
		if self.role == "Jäger":
			activate_jaeger(context, self, game_id)
		elif self.role == "Terrorwolf":
			activate_terrorwolf(context, self, game_id)

def get_player_by_id(user_id, game_id):
	for player in game_dict[game_id]["player_list"]:
		if str(player.user_id) == str(user_id) and player.alive:
			return player
	return None

def get_player_by_role(role, game_id):
	for player in game_dict[game_id]["player_list"]:
		if player.role == role and player.alive:
			return player
	return None

def get_alive_player_list(game_id):
	alive_player_list = []
	for player in game_dict[game_id]["player_list"]:
		if player.alive:
			alive_player_list.append(player)
	return alive_player_list

class Prosecuted:
	def __init__(self, user_id, by_id):
		self.user_id = user_id
		self.by_id = by_id
		self.option = ""

def inlineKey_menu(game_id):
	keyboard = [[InlineKeyboardButton("Mitspielen/Aussteigen", callback_data='menu_1_'+str(game_id))],
				[InlineKeyboardButton("Start", callback_data='menu_2_'+str(game_id)),
				InlineKeyboardButton("Abbrechen", callback_data='menu_3_'+str(game_id))]]
	return InlineKeyboardMarkup(keyboard)

def inlineKey_werwolf(game_id):
	keyboard = []
	for player in get_alive_player_list(game_id):
		(text_id, text) = lore.inlineKey_werwolf_options(player.name)
		keyboard.append([InlineKeyboardButton(text, callback_data="werwolf_" + str(player.user_id)+"_"+str(text_id)+"_"+str(game_id))])
	(text_id, text) = lore.inlineKey_werwolf_options("Niemanden")
	keyboard.append([InlineKeyboardButton(text, callback_data="werwolf_-1_"+str(text_id)+"_"+str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def inlineKey_anklage(game_id):
	keyboard = []
	for player in get_alive_player_list(game_id):
		(text_id, text) = lore.anklage_options()
		keyboard.append([InlineKeyboardButton(player.name + text, callback_data="anklage_" + str(player.user_id)+"_" + str(text_id) + "_" +str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def inlineKey_abstimmung(game_id):
	keyboard = []
	for player in game_dict[game_id]["anklage_list"]:
		for p in get_alive_player_list(game_id):
			if str(p.user_id) == str(player.user_id):
				(text_id, text) = lore.vote_options()
				keyboard.append([InlineKeyboardButton(p.name + text, callback_data="vote_" + str(player.user_id)+"_" + str(text_id) + "_" +str(game_id))])
				break
	return InlineKeyboardMarkup(keyboard)

def inlineKey_jaeger(p, game_id):
	keyboard = []
	for player in get_alive_player_list(game_id):
		if str(player.user_id) != str(p.user_id) and not player.marked_by_werwolf and not player.marked_by_witch:
			(text_id, text) = lore.inlineKey_jaeger_options()
			keyboard.append([InlineKeyboardButton(player.name + text, callback_data="jaeger_" + str(player.user_id)+"_" + str(text_id) + "_" +str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def inlineKey_terrorwolf(p, game_id):
	keyboard = []
	for player in get_alive_player_list(game_id):
		if str(player.user_id) != str(p.user_id) and not player.marked_by_werwolf and not player.marked_by_witch:
			(text_id, text) = lore.inlineKey_terrorwolf_options()
			keyboard.append([InlineKeyboardButton(player.name + text, callback_data="terrorwolf_" + str(player.user_id)+"_" + str(text_id) + "_" +str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def inlineKey_seherin(game_id):
	keyboard = []
	for player in get_alive_player_list(game_id):
		if player.role != "Seherin":
			(text_id, text) = lore.seherin_options(player.name)
			keyboard.append([InlineKeyboardButton(text, callback_data="seherin_" + str(player.user_id)+"_" + str(text_id) + "_" +str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def inlineKey_hexe_life(game_id):
	keyboard = []
	(hexe_save_id, hexe_save_lore) = lore.hexe_save()
	(hexe_let_die_id, hexe_let_die_lore) = lore.hexe_let_die()
	keyboard.append([InlineKeyboardButton(hexe_save_lore, callback_data="hexe_life1_"+str(hexe_save_id)+"_"+str(game_id))])
	keyboard.append([InlineKeyboardButton(hexe_let_die_lore, callback_data="hexe_life0_"+str(hexe_let_die_id)+"_"+str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def inlineKey_hexe_death(game_id):
	keyboard = []
	for player in get_alive_player_list(game_id):
		(hexe_kill_id, hexe_kill_lore) = lore.hexe_kill()
		keyboard.append([InlineKeyboardButton(player.name + hexe_kill_lore, callback_data="hexedeath_" + str(player.user_id) + "_" +str(hexe_kill_id) + "_" + str(game_id))])
	(hexe_kill_id, hexe_kill_lore) = lore.hexe_kill()
	keyboard.append([InlineKeyboardButton("Niemanden" + hexe_kill_lore, callback_data="hexedeath_0_" +str(hexe_kill_id) + "_" +  str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def inlineKey_wolfshund(game_id):
	keyboard = []
	(wolfshund_option_werwolf, wolfshund_lore_werwolf) = lore.wolfshund_choose_werwolf()
	(wolfshund_option_dorf, wolfshund_lore_dorf) = lore.wolfshund_choose_dorf()
	keyboard.append([InlineKeyboardButton(wolfshund_lore_werwolf, callback_data="wolfshund_werwolf_" + str(wolfshund_option_werwolf) + "_" + str(game_id))])
	keyboard.append([InlineKeyboardButton(wolfshund_lore_dorf, callback_data="wolfshund_dorf_" + str(wolfshund_option_dorf) + "_" + str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def inlineKey_psychopath(game_id):
	keyboard = []
	for player in get_alive_player_list(game_id):
		(psychopath_kill_option, psychopath_kill_lore) = lore.inlineKey_psychopath_options(player.name)
		keyboard.append([InlineKeyboardButton(psychopath_kill_lore, callback_data="psychopath_" + str(player.user_id) + "_" +str(psychopath_kill_option) + "_" + str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def draw_no_doubles(context, game_id):
	global game_dict
	random.shuffle(game_dict[game_id]["player_list"])
	werwolf_role_list = []
	if len(game_dict[game_id]["player_list"]) >= 6:
		for i in range(0,20):
			werwolf_role_list.append("Werwolf")
		for i in range(0,40):
			werwolf_role_list.append("Wolfshund")
	else:
		for i in range(0,60):
			werwolf_role_list.append("Werwolf")
	for i in range(0,40):
		werwolf_role_list.append("Terrorwolf")

	dorf_role_list = []
	for i in range(0,12):
		dorf_role_list.append("Dorfbewohner")
		dorf_role_list.append("Dorfbewohnerin")
	for i in range(0,15):
		dorf_role_list.append("Jäger")
	for i in range(0,15):
		dorf_role_list.append("Seherin")
	for i in range(0,16):
		dorf_role_list.append("Hexe")
	for i in range(0,15):
		dorf_role_list.append("HarterBursche")
	for i in range(0,15):
		dorf_role_list.append("Psychopath")

	unique = ["Jäger", "Seherin", "Hexe", "Rotkäppchen", "HarterBursche", "Wolfshund", "Terrorwolf", "Psychopath"]

	for i,p in enumerate(game_dict[game_id]["player_list"]):
		group_mod = random.random()*0.2+0.9
		werwolf_amount = int(round(len(game_dict[game_id]["player_list"])*(1.0/3.5)*group_mod, 0))
		if i<werwolf_amount:
			role = random.randrange(0,len(werwolf_role_list))
			p.role = werwolf_role_list[role]
			if werwolf_role_list[role] in unique:
				while p.role in werwolf_role_list:
					werwolf_role_list.remove(p.role)
		else:
			role = random.randrange(0,len(dorf_role_list))
			p.role = dorf_role_list[role]
			if p.role == "Jäger":
				for i in range(0,20):
					dorf_role_list.append("Rotkäppchen")
			if dorf_role_list[role] in unique:
				while p.role in dorf_role_list:
					dorf_role_list.remove(p.role)

		if p.role == "Werwolf": context.bot.send_message(chat_id=p.user_id, text=lore.description_werwolf())
		elif p.role == "Wolfshund": context.bot.send_message(chat_id=p.user_id, text=lore.description_wolfshund())
		elif p.role == "Terrorwolf": context.bot.send_message(chat_id=p.user_id, text=lore.description_terrorwolf())
		elif p.role == "Dorfbewohner": context.bot.send_message(chat_id=p.user_id, text=lore.description_dorfbewohner())
		elif p.role == "Dorfbewohnerin": context.bot.send_message(chat_id=p.user_id, text=lore.description_dorfbewohnerin())
		elif p.role == "Hexe": context.bot.send_message(chat_id=p.user_id, text=lore.description_hexe())
		elif p.role == "Seherin": context.bot.send_message(chat_id=p.user_id, text=lore.description_seherin())
		elif p.role == "Jäger": context.bot.send_message(chat_id=p.user_id, text=lore.description_jaeger())
		elif p.role == "Rotkäppchen": context.bot.send_message(chat_id=p.user_id, text=lore.description_rotkaeppchen())
		elif p.role == "HarterBursche": context.bot.send_message(chat_id=p.user_id, text=lore.description_harter_bursche())
		elif p.role == "Psychopath": context.bot.send_message(chat_id=p.user_id, text=lore.description_psychopath())
	random.shuffle(game_dict[game_id]["player_list"])

def game_over(context, game_id):
	global game_dict
	if not game_dict[game_id]["game_over_check"]:
		if len(get_alive_player_list(game_id)) == 0:
			game_dict[game_id]["admin_id"] = 0
			game_dict[game_id]["running"] = False
			all_dead_message = lore.all_dead()
			context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=markup_character + lall_dead_message + markup_character, parse_mode=ParseMode.MARKDOWN_V2)
			for player in game_dict[game_id]["player_list"]:
				context.bot.send_message(chat_id=player.user_id, text=markup_character + all_dead_message + markup_character, parse_mode=ParseMode.MARKDOWN_V2)
			game_dict[game_id]["game_over_check"] = True
			game_dict[game_id]["state"] = None
			game_dict[game_id]["player_list"] = []
			return True
		if not game_dict[game_id]["single_player"]:
			if get_alive_player_list(game_id)[0].role in werwolf_group: group = werwolf_group
			else: group = dorf_group
			over = True
			for p in get_alive_player_list(game_id):
				if p.role not in group:
					over = False
			if over:
				game_dict[game_id]["admin_id"] = 0
				game_dict[game_id]["running"] = False
				if group == werwolf_group: 
					win_message = markup_character + lore.werwoelfe_win().upper() + markup_character
				else: 
					win_message = markup_character + lore.dorf_win().upper() + markup_character
				context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=win_message, parse_mode=ParseMode.MARKDOWN_V2)
				for player in game_dict[game_id]["player_list"]:
					context.bot.send_message(chat_id=player.user_id, text=win_message, parse_mode=ParseMode.MARKDOWN_V2)
				game_dict[game_id]["game_over_check"] = True
				game_dict[game_id]["state"] = None
				game_dict[game_id]["player_list"] = []
				return True
		return False

def wake_werwolf(context, game_id):
	global game_dict
	if get_player_by_role("Werwolf", game_id) == None and get_player_by_role("Terrorwolf", game_id) == None: return
	game_dict[game_id]["game_state"] = "werwolf"
	werwolf_keyboard = inlineKey_werwolf(game_id)
	werwolf_introduction = lore.werwolf_choose_target()
	for p in get_alive_player_list(game_id):
		if p.role in werwolf_group:
			werwolf_tmp_list = []
			for tmp in get_alive_player_list(game_id):
				if tmp.role in werwolf_group and tmp.user_id != p.user_id:
					werwolf_tmp_list.append(tmp.name)
			if len(werwolf_tmp_list) > 0:
				message = "Werwölfe sind du, "
				for i in range(0,len(werwolf_tmp_list)-1):
					message += werwolf_tmp_list[i] + ", "
				message = message[0:-2] + " und " + werwolf_tmp_list[len(werwolf_tmp_list)-1] + "."
				context.bot.send_message(chat_id=p.user_id, text=message)
			else:
				context.bot.send_message(chat_id=p.user_id, text=lore.lonely_wolf())
			context.bot.send_message(chat_id=p.user_id, text=werwolf_introduction, reply_markup=werwolf_keyboard)
	while game_dict[game_id]["game_state"] == "werwolf":
			time.sleep(1)
			print("waiting")
	if get_player_by_role("Rotkäppchen", game_id) != None and get_player_by_role("Rotkäppchen", game_id).marked_by_werwolf and get_player_by_role("Jäger", game_id).alive:
		get_player_by_role("Rotkäppchen", game_id).marked_by_werwolf = False
	if get_player_by_role("HarterBursche", game_id) != None and game_dict[game_id]["harter_bursche_survive"] and get_player_by_role("HarterBursche", game_id).marked_by_werwolf:
		game_dict[game_id]["harter_bursche_survive"] = False
		get_player_by_role("HarterBursche", game_id).marked_by_werwolf = False

def activate_jaeger(context, p, game_id):
	global game_dict
	game_dict[game_id]["game_state_backup"] = game_dict[game_id]["game_state"]
	game_dict[game_id]["game_state"] = "jaeger"
	context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=p.name + lore.jaeger_reveal())
	context.bot.send_message(chat_id=p.user_id, text=lore.jaeger_choose_target(), reply_markup=inlineKey_jaeger(p, game_id))
	while game_dict[game_id]["game_state"] == "jaeger" or game_dict[game_id]["game_state_backup"] == "jaeger":
		time.sleep(1)
		print("jaeger_waiting")

def activate_terrorwolf(context, p, game_id):
	global game_dict
	game_dict[game_id]["game_state_backup"] = game_dict[game_id]["game_state"]
	game_dict[game_id]["game_state"] = "terrorwolf"
	context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=p.name + lore.terrorwolf_reveal())
	context.bot.send_message(chat_id=p.user_id, text=lore.terrorwolf_choose_target(), reply_markup=inlineKey_terrorwolf(p, game_id))
	while game_dict[game_id]["game_state"] == "terrorwolf" or game_dict[game_id]["game_state_backup"] == "terrorwolf":
		time.sleep(1)
		print("terrorwolf_waiting")

def wake_seherin(context, game_id):
	global game_dict
	if get_player_by_role("Seherin", game_id) == None: return
	seherin = get_player_by_role("Seherin", game_id)
	context.bot.send_message(chat_id=seherin.user_id, text=lore.seherin_choose_target(), reply_markup=inlineKey_seherin(game_id))
	game_dict[game_id]["game_state"] = "seherin"
	while game_dict[game_id]["game_state"] == "seherin":
		time.sleep(1)

def wake_hexe(context, game_id):
	if get_player_by_role("Hexe", game_id) == None: return
	global game_dict
	if not game_dict[game_id]["hexe_life_juice_used"]:
		victim_name = ""
		for player in get_alive_player_list(game_id):
			if player.marked_by_werwolf:
				victim_name = player.name
		if victim_name != "":
			context.bot.send_message(chat_id=get_player_by_role("Hexe", game_id).user_id, text=victim_name + " wurde diese Nacht von den Werwölfen erwischt. Möchtest du diese Person retten?", reply_markup=inlineKey_hexe_life(game_id))
			game_dict[game_id]["game_state"] = "hexe_life"
			while game_dict[game_id]["game_state"] == "hexe_life":
				time.sleep(1)
	if not game_dict[game_id]["hexe_death_juice_used"]:
		game_dict[game_id]["game_state"] = "hexe_death"
		context.bot.send_message(chat_id=get_player_by_role("Hexe", game_id).user_id, text="Willst du noch jemanden töten?", reply_markup=inlineKey_hexe_death(game_id))
		while game_dict[game_id]["game_state"] == "hexe_death":
				time.sleep(1)

def wake_wolfshund(context, game_id):
	global game_dict
	if get_player_by_role("Wolfshund", game_id) == None: return
	game_dict[game_id]["game_state"] = "wolfshund"
	context.bot.send_message(chat_id=get_player_by_role("Wolfshund", game_id).user_id, text=lore.wolfshund_options(), reply_markup=inlineKey_wolfshund(game_id))
	while game_dict[game_id]["game_state"] == "wolfshund":
		time.sleep(1)

def wake_psychopath(context, game_id):
	global game_dict
	if get_player_by_role("Psychopath", game_id) == None: return
	for player in get_alive_player_list(game_id):
		if player.marked_by_werwolf or player.marked_by_witch: return
	game_dict[game_id]["game_state"] = "psychopath"
	context.bot.send_message(get_player_by_role("Psychopath", game_id), text=lore.psycho_intro(), reply_markup=inlineKey_psychopath(game_id))
	while game_dict[game_id]["game_state"] == "psychopath":
		time.sleep(1)

def do_killing(context, game_id):
	global game_dict
	do_killing_list = []
	for p in get_alive_player_list(game_id):
		if p.marked_by_werwolf or p.marked_by_witch or p.marked_by_psychopath:
			death_message = lore.death_message()
			context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=markup_character + p.name + death_message + markup_character, parse_mode=ParseMode.MARKDOWN_V2)
			context.bot.send_message(chat_id=p.user_id, text=markup_character + p.name + death_message + markup_character, parse_mode=ParseMode.MARKDOWN_V2)
			p.kill(context, game_id)
			p.marked_by_werwolf = False
			p.marked_by_witch = False
			p.marked_by_psychopath = False

def print_alive(context, game_id):
	message = "Es leben noch: "
	if len(get_alive_player_list(game_id)) == 1:
		message = "Es lebt noch: "
	for p in get_alive_player_list(game_id):
		message += p.name + ", "
	context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=message[0:-2])

def prosecute(context, game_id):
	global game_dict
	context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=lore.time_to_prosecute(), reply_markup=inlineKey_anklage(game_id))
	while len(game_dict[game_id]["anklage_list"]) < 3 and len(game_dict[game_id]["anklage_list"]) < len(get_alive_player_list(game_id)):
		time.sleep(1)

def vote(context, game_id):
	global game_dict
	kill_list = []
	context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=lore.time_to_vote(), reply_markup=inlineKey_abstimmung(game_id))
	while len(game_dict[game_id]["vote_list"]) < len(get_alive_player_list(game_id)):
		time.sleep(1)
	vote_dict = {}
	for v in game_dict[game_id]["vote_list"]:
		try:
			vote_dict[str(v.user_id)] +=1
		except Exception as e:
			vote_dict[str(v.user_id)] =1
	max_vote = 0
	for v in vote_dict:
		if vote_dict[v] > max_vote:
			kill_list = [v]
			max_vote = vote_dict[v]
		elif vote_dict[v] == max_vote:
			kill_list.append(v)
	if len(kill_list) == 1:
		kill_player = get_player_by_id(kill_list[0], game_id)
		sentence = lore.vote_judgement(game_dict[game_id]["vote_options"][str(kill_player.user_id)])
		context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=markup_character + kill_player.name + sentence + markup_character, parse_mode=ParseMode.MARKDOWN_V2)
		kill_player.kill(context, game_id)
	else:
		if game_dict[game_id]["first_patt"]:
			game_dict[game_id]["first_patt"] = False
			context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=lore.patt_revote())
			game_dict[game_id]["anklage_list"] = []
			for v in game_dict[game_id]["vote_list"]:
				if v.user_id in kill_list:
					already_in = False
					for a in game_dict[game_id]["anklage_list"]:
						if str(v.user_id) == str(a.user_id):
							already_in = True
					if not already_in:
						game_dict[game_id]["anklage_list"].append(v)
			game_dict[game_id]["vote_list"] = []
			game_dict[game_id]["vote_message_id"] = 0
			game_dict[game_id]["vote_text"] = {}
			vote(context, game_id)
		else:
			game_dict[game_id]["first_patt"] = True
			context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=lore.patt_no_kill())

def test_chats(context, game_id):
	success = True
	for player in game_dict[game_id]["player_list"]:
		try:
			test_id = context.bot.send_message(chat_id=player.user_id, text="Herzlich Willkommen bei einem neuen Werwolf-Spiel!").message_id
			context.bot.delete_message(chat_id=player.user_id, message_id=test_id)
		except Unauthorized:
			context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=player.name + ", bitte beginne einen privaten Chat mit mir!")
			success = False
	return success

def start_game(context, game_id):
	global game_dict
	game_dict[game_id]["game_over_check"] = False
	draw_no_doubles(context, game_id)
	while not game_over(context, game_id) and not game_dict[game_id]["game_over_check"]:
		game_dict[game_id]["werwolf_target_list"] = []
		game_dict[game_id]["vote_list"] = []
		game_dict[game_id]["anklage_list"] = []
		game_dict[game_id]["game_state"] = "night"
		game_dict[game_id]["werwolf_target"] = "0"
		for player in game_dict[game_id]["player_list"]:
			player.werwolf_message_id = 0
		game_dict[game_id]["werwolf_text"] = {}
		game_dict[game_id]["anklage_text"] = {}
		game_dict[game_id]["vote_text"] = {}
		game_dict[game_id]["anklgage_message_id"] = 0
		game_dict[game_id]["vote_message_id"] = 0

		text_nightfall = lore.nightfall()
		context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=text_nightfall)
		for p in get_alive_player_list(game_id):
			context.bot.send_message(chat_id=p.user_id, text=text_nightfall)

		if game_dict[game_id]["round_number"] == 0:
			wake_wolfshund(context, game_id)
		wake_seherin(context, game_id)
		wake_werwolf(context, game_id)
		wake_hexe(context, game_id)
		wake_psychopath(context, game_id)
		do_killing(context, game_id)

		#night is over
		if not game_over(context, game_id):
			if len(get_alive_player_list(game_id))>3:
				game_dict[game_id]["game_state"] = "anklage"
				prosecute(context, game_id)
			else:
				for p in get_alive_player_list(game_id):
					game_dict[game_id]["anklage_list"].append(p)
			game_dict[game_id]["game_state"] = "vote"
			vote(context, game_id)
			game_dict[game_id]["round_number"] += 1

def button_handler_menu(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data[7::]
	if query.data.startswith("menu_1"):
		if game_dict[game_id]["admin_id"] != 0:
			if game_dict[game_id]["running"]:
				context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text="Spiel läuft bereits!")
			else:
				active = False
				for p in game_dict[game_id]["player_list"]:
					if p.user_id == query.from_user.id: active = True
				if not active:
					game_dict[game_id]["player_list"].append(Spieler(query.from_user.id, query.from_user.first_name))
					message = query.message.text
					message += "\n" + query.from_user.first_name
					context.bot.edit_message_text(text=message, chat_id=game_dict[game_id]["game_chat_id"], message_id=query.message.message_id, reply_markup=inlineKey_menu(game_id))
				else:
					for p in game_dict[game_id]["player_list"]:
						if p.user_id == query.from_user.id:
							game_dict[game_id]["player_list"].remove(p)
							break
					message = query.message.text
					lines = message.split("\n")
					new_message = ""
					i = 0
					while not lines[i].startswith("Spieler:"):
						new_message += lines[i] + "\n"
						i+=1
					new_message += "Spieler:\n"
					for p in game_dict[game_id]["player_list"]:
						new_message+= p.name + "\n"
					new_message = new_message[0:-1]
					context.bot.edit_message_text(text=new_message, chat_id=game_dict[game_id]["game_chat_id"], message_id=query.message.message_id, reply_markup=inlineKey_menu(game_id))
	elif query.data.startswith("menu_2"):
		if query.from_user.id != game_dict[game_id]["admin_id"]:
			context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text="Du bist nicht der Administrator dieses Spieles")
		elif len(game_dict[game_id]["player_list"]) < 4 and not game_dict[game_id]["single_player"]:
			context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text="Zu wenige Mitspieler!")
		elif game_dict[game_id]["running"]:
			context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text="Spiel läuft bereits!")
		else: 
			if not test_chats(context, game_id):
				return
			game_dict[game_id]["running"] = True
			context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=lore.get_lore())
			game = threading.Thread(target=start_game, args=(context,game_id,))
			game.start()
	elif query.data.startswith("menu_3"):
		if query.from_user.id != game_dict[game_id]["admin_id"]:
			context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text="Du bist nicht der Administrator dieses Spieles")
		else:
			context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text="Abgebrochen")
			game_dict.pop(game_id)

def handler_send_message(update, context, game_id, lore_text, user_id, text_dict, saved_message_id):
	global game_dict
	if str(user_id) in game_dict[game_id][text_dict]:
		game_dict[game_id][text_dict][str(user_id)] += lore_text + "\n"
	else:
		game_dict[game_id][text_dict][str(user_id)] = lore_text + "\n"
	new_text = ""
	for text in game_dict[game_id][text_dict]:
		new_text += game_dict[game_id][text_dict][text] + "\n"
	if saved_message_id == "werwolf_message_id":
		for player in get_alive_player_list(game_id):
			if str(player.user_id) == str(user_id):
				if player.werwolf_message_id == 0:
					player.werwolf_message_id = context.bot.send_message(chat_id=user_id, text=new_text).message_id
				else:
					context.bot.edit_message_text(chat_id=user_id, message_id=player.werwolf_message_id, text=new_text)
	else:
		if game_dict[game_id][saved_message_id] == 0:
			game_dict[game_id][saved_message_id] = context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=new_text).message_id
		else:
			context.bot.edit_message_text(chat_id=game_dict[game_id]["game_chat_id"], message_id=game_dict[game_id][saved_message_id], text=new_text)

def button_handler_werwolf(update, context):
	global game_dict
	werwolf_list = []
	query = update.callback_query
	game_id = query.data.split("_")[3]
	killing_option = query.data.split("_")[2]
	if not game_dict[game_id]["game_state"] == "werwolf": return
	for p in get_alive_player_list(game_id):
		if p.role in werwolf_group:
			werwolf_list.append(p)
	if query.data.startswith("werwolf_-1"):
		for w in werwolf_list:
			lore_text = query.from_user.first_name + " schlägt vor, " + lore.werwolf_response_options(killing_option, "niemanden")
			handler_send_message(update, context, game_id, lore_text, w.user_id, "werwolf_text", "werwolf_message_id")
		player_in_list = False
		for t in game_dict[game_id]["werwolf_target_list"]:
			if t.wolf_id == query.from_user.id:
				player_in_list = True
				t.target_id = "-1"
		if not player_in_list:
			game_dict[game_id]["werwolf_target_list"].append(Target(query.from_user.id, "-1"))
	else:
		target_id = query.data.split("_")[1]
		player_in_list = False
		for w in game_dict[game_id]["werwolf_target_list"]:
			if w.wolf_id == query.from_user.id:
				w.target_id = target_id
				player_in_list = True
		if not player_in_list:
			game_dict[game_id]["werwolf_target_list"].append(Target(query.from_user.id, target_id))
		target_name = get_player_by_id(target_id, game_id).name
		for w in werwolf_list:
			lore_text = query.from_user.first_name + " schlägt vor, " + lore.werwolf_response_options(killing_option, target_name)
			handler_send_message(update, context, game_id, lore_text, w.user_id, "werwolf_text", "werwolf_message_id")
	if len(werwolf_list) == len(game_dict[game_id]["werwolf_target_list"]) and len(werwolf_list) != 0:
		same = True
		first_target = game_dict[game_id]["werwolf_target_list"][0]
		for t in game_dict[game_id]["werwolf_target_list"]:
			if not t.target_id == first_target.target_id:
				same = False
				break
		print("same")
		print(same)
		if same:
			get_player_by_id(first_target.target_id, game_id).marked_by_werwolf = True
			if first_target.target_id == "-1": target_name = "niemanden"
			for w in werwolf_list:
				context.bot.send_message(chat_id=w.user_id, text="Die Werwölfe haben beschlossen, " + lore.werwolf_response_options(killing_option, target_name))
			game_dict[game_id]["game_state"] = "night"


def button_handler_anklage(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[3]
	anklage_option = query.data.split("_")[2]
	if not game_dict[game_id]["game_state"] == "anklage": return
	p = get_player_by_id(query.from_user.id, game_id)
	anklage_id = query.data.split("_")[1]
	anklage_in_list = False
	for a in game_dict[game_id]["anklage_list"]:
		if str(a.user_id) == anklage_id: anklage_in_list = True
	anklaeger_name = get_player_by_id(query.from_user.id, game_id).name
	angeklagter_name = get_player_by_id(anklage_id, game_id).name
	if not anklage_in_list:
		anklaeger_in_list = False
		for a in game_dict[game_id]["anklage_list"]:
			if str(a.by_id) == str(query.from_user.id):
				a.user_id = anklage_id
				anklaeger_in_list = True
				lore_text = anklaeger_name + lore.anklage_change(anklage_option, angeklagter_name)
				handler_send_message(update, context, game_id, lore_text, query.from_user.id, "anklage_text", "anklage_message_id")
				break
		if not anklaeger_in_list:
			game_dict[game_id]["anklage_list"].append(Prosecuted(anklage_id, query.from_user.id))
			lore_text = anklaeger_name + lore.anklage_new(anklage_option, angeklagter_name)
			handler_send_message(update, context, game_id, lore_text, query.from_user.id, "anklage_text", "anklage_message_id")

def button_handler_vote(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[3]
	vote_option = query.data.split("_")[2]
	if not game_dict[game_id]["game_state"] == "vote": return
	user_allowed = False
	p = get_player_by_id(query.from_user.id, game_id)
	vote_id = query.data.split("_")[1]
	already_voted = False
	voter_name = get_player_by_id(query.from_user.id, game_id).name
	voted_name = get_player_by_id(vote_id, game_id).name
	game_dict[game_id]["vote_options"].update({str(vote_id):vote_option})			
	for v in game_dict[game_id]["vote_list"]:
		if str(v.by_id) == str(query.from_user.id):
			already_voted = True
			v.user_id = vote_id
			lore_text = voter_name + lore.vote_change(vote_option, voted_name)
			handler_send_message(update, context, game_id, lore_text, query.from_user.id, "vote_text", "vote_message_id")
			game_dict[game_id]["last_vote_option"] = vote_option
			break
	if not already_voted:
		game_dict[game_id]["vote_list"].append(Prosecuted(vote_id, query.from_user.id))
		lore_text = voter_name + lore.vote_new(vote_option, voted_name)
		handler_send_message(update, context, game_id, lore_text, query.from_user.id, "vote_text", "vote_message_id")
		game_dict[game_id]["last_vote_option"] = vote_option

def button_handler_terrorwolf(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[3]
	print(game_dict[game_id]["game_state"])
	if not game_dict[game_id]["game_state"] == "terrorwolf": return
	kill_option = query.data.split("_")[2]
	kill_id = query.data.split("_")[1]
	kill_player = get_player_by_id(kill_id, game_id)

	context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=markup_character + kill_player.name + lore.terrorwolf_kill(kill_option) + markup_character, parse_mode=ParseMode.MARKDOWN_V2)
	context.bot.send_message(chat_id=kill_id, text=markup_character + kill_player.name + lore.terrorwolf_kill(kill_option) + markup_character, parse_mode=ParseMode.MARKDOWN_V2) 
	
	kill_player.kill(context, game_id)

	game_dict[game_id]["game_state"] = game_dict[game_id]["game_state_backup"]
	game_dict[game_id]["game_state_backup"] = None
	print(game_dict[game_id]["game_state"])
	print(game_dict[game_id]["game_state_backup"])

def button_handler_jaeger(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[3]
	print(game_dict[game_id]["game_state"])
	if not game_dict[game_id]["game_state"] == "jaeger": return
	kill_option = query.data.split("_")[2]
	kill_id = query.data.split("_")[1]
	kill_player = get_player_by_id(kill_id, game_id)

	context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=markup_character + kill_player.name + lore.jaeger_shot(kill_option) + markup_character, parse_mode=ParseMode.MARKDOWN_V2)
	context.bot.send_message(chat_id=kill_id, text=markup_character + kill_player.name + lore.jaeger_shot(kill_option) + markup_character, parse_mode=ParseMode.MARKDOWN_V2) 
	
	kill_player.kill(context, game_id)

	game_dict[game_id]["game_state"] = game_dict[game_id]["game_state_backup"]
	game_dict[game_id]["game_state_backup"] = None
	print(game_dict[game_id]["game_state"])
	print(game_dict[game_id]["game_state_backup"])

def button_handler_seherin(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[3]
	seherin_option = query.data.split("_")[2]
	watch_id = query.data.split("_")[1]
	if game_dict[game_id]["game_state"] != "seherin": return
	watch_in_list = False
	seherin = get_player_by_role("Seherin", game_id)

	if get_player_by_id(watch_id, game_id).role in werwolf_group:
		context.bot.send_message(chat_id=seherin.user_id, text=lore.seherin_werwolf(seherin_option, get_player_by_id(watch_id, game_id).name))
	else:
		context.bot.send_message(chat_id=seherin.user_id, text=lore.seherin_no_werwolf(seherin_option, get_player_by_id(watch_id, game_id).name))
	game_dict[game_id]["game_state"] = "night"		

def button_handler_hexe_life(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[3]
	save_option = query.data.split("_")[2]
	if game_dict[game_id]["game_state"] != "hexe_life": return
	for player in get_alive_player_list(game_id):
		if player.marked_by_werwolf:
			hit_player = player
	if query.data.startswith("hexe_life0_"):
		context.bot.send_message(chat_id=get_player_by_role("Hexe", game_id).user_id, text=lore.hexe_did_let_die(save_option, player.name))
		game_dict[game_id]["game_state"] = "night"
	elif query.data.startswith("hexe_life1_"):
		game_dict[game_id]["hexe_life_juice_used"] = True
		for player in get_alive_player_list(game_id):
			player.marked_by_werwolf = False
		context.bot.send_message(chat_id=get_player_by_role("Hexe", game_id).user_id, text=lore.hexe_did_save(save_option, player.name))
		game_dict[game_id]["game_state"] = "night"

def button_handler_hexe_death(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[3]
	kill_option = query.data.split("_")[2]
	if game_dict[game_id]["game_state"] != "hexe_death": return
	if query.data.startswith("hexedeath_0_"):
		context.bot.send_message(chat_id=get_player_by_role("Hexe", game_id).user_id, text=lore.hexe_did_kill(kill_option, "niemanden"))
		game_dict[game_id]["game_state"] = "night"
		return
	elif query.data.startswith("hexedeath_"):
		hexe_target_id = query.data.split("_")[1]
		get_player_by_id(hexe_target_id, game_id).marked_by_witch = True
		context.bot.send_message(chat_id=get_player_by_role("Hexe", game_id).user_id, text=lore.hexe_did_kill(kill_option, get_player_by_id(hexe_target_id, game_id).name))
		game_dict[game_id]["hexe_death_juice_used"] = True
		game_dict[game_id]["game_state"] = "night"

def button_handler_wolfshund_choose(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[3]
	wolfshund_option = query.data.split("_")[2]
	if not game_dict[game_id]["game_state"] == "wolfshund": return
	target = query.data.split("_")[1]
	if target == "werwolf":
		context.bot.send_message(chat_id=get_player_by_role("Wolfshund", game_id).user_id, text=lore.wolfshund_did_chose_werwolf(wolfshund_option))
		get_player_by_role("Wolfshund", game_id).role = "Werwolf"
	elif target == "dorf":
		context.bot.send_message(chat_id=get_player_by_role("Wolfshund", game_id).user_id, text=lore.wolfshund_did_chose_dorf(wolfshund_option))
		get_player_by_role("Wolfshund", game_id).role = "Dorfbewohner"
	game_dict[game_id]["game_state"] = "night"

def button_handler_psychopath(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[3]
	psychopath_option = query.data.split("_")[2]
	if not game_dict[game_id]["game_state"] == "psychopath": return
	target = query.data.split("_")[1]
	get_player_by_id(target, game_id).marked_by_psychopath = True
	context.bot.send_message(chat_id=get_player_by_role("Psychopath", game_id).user_id, text=lore.psyhopath_response_options(psychopath_option, get_player_by_id(target, game_id).name))
	game_dict[game_id]["game_state"] = "psychopath"

def button_handler(update, context):
	if update.callback_query.data.startswith("menu_"):
		threading.Thread(target=button_handler_menu, args=(update,context,)).start()
	elif update.callback_query.data.startswith("werwolf_"):
		threading.Thread(target=button_handler_werwolf, args=(update,context,)).start()
	elif update.callback_query.data.startswith("anklage_"):
		threading.Thread(target=button_handler_anklage, args=(update,context,)).start()
	elif update.callback_query.data.startswith("vote_"):
		threading.Thread(target=button_handler_vote, args=(update,context,)).start()
	elif update.callback_query.data.startswith("jaeger_"):
		threading.Thread(target=button_handler_jaeger, args=(update,context,)).start()
	elif update.callback_query.data.startswith("terrorwolf_"):
		threading.Thread(target=button_handler_terrorwolf, args=(update,context,)).start()
	elif update.callback_query.data.startswith("seherin_"):
		threading.Thread(target=button_handler_seherin, args=(update,context,)).start()
	elif update.callback_query.data.startswith("hexe_life"):
		threading.Thread(target=button_handler_hexe_life, args=(update,context,)).start()
	elif update.callback_query.data.startswith("hexedeath_"):
		threading.Thread(target=button_handler_hexe_death, args=(update,context,)).start()
	elif update.callback_query.data.startswith("wolfshund_"):
		threading.Thread(target=button_handler_wolfshund_choose, args=(update,context,)).start()

def new(update, context):
	global game_dict
	game_id = secrets.token_hex(16)
	print(game_id)
	new_game = {}
	for key in game_library:
		new_game.update({key:game_library[key]})
	game_dict.update({game_id:new_game})
	game_dict[game_id]["player_list"] = []
	game_dict[game_id]["admin_id"] = update.message.from_user.id
	game_dict[game_id]["game_chat_id"] = update.message.chat_id
	message = "Viel Spass beim Werwolf spielen!\n\nBitte einen privaten Chat mit dem Bot starten, bevor das Spiel beginnt!\n\nUm das Spiel in seiner vollen Breite genießen zu können, empfiehlt es sich bei sehr schmalen Bildschirmen, diese quer zu verwenden.\n\n"
	message += "Admin:\n" + update.message.from_user.first_name + "\n\n"
	message += "Spieler:"
	context.bot.send_message(chat_id=update.message.chat_id, text=message, reply_markup=inlineKey_menu(game_id))

def start(update, context):
	test = context.bot.send_message(chat_id=update.message.chat_id, text="Herzlich Wilkommen beim WerWolfBot\\!", parse_mode=ParseMode.MARKDOWN_V2).message_id

def main():
	updater = Updater(token, use_context=True)
	dispatcher = updater.dispatcher
	dispatcher.add_handler(CommandHandler('start',start))
	dispatcher.add_handler(CommandHandler('new',new))
	dispatcher.add_handler(CallbackQueryHandler(button_handler))
	updater.start_polling()
	updater.idle()
    
if __name__ == '__main__':
    main()