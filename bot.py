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
				"fast_game":1,
				"allow_double_role":0,
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
				"harter_bursche_survive" : True}

werwolf_group = ["Werwolf"]
dorf_group = ["Dorfbewohner", "Dorfbewohnerin", "Jäger", "Seherin", "Hexe", "Rotkäppchen", "HarterBursche"]

class Target:
	def __init__(self, wolf_id, target_id):
		self.wolf_id = wolf_id
		self.target_id = target_id

class Spieler:
	def __init__(self, user_id, name):
		self.name = name
		self.user_id = user_id
		self.role = None

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
	for player in game_dict[game_id]["player_list"]:
		(text_id, text) = lore.inlineKey_werwolf_options(player.name)
		print("werwolf_" + str(player.user_id)+"_"+str(text_id)+"_"+str(game_id))
		keyboard.append([InlineKeyboardButton(text, callback_data="werwolf_" + str(player.user_id)+"_"+str(text_id)+"_"+str(game_id))])
	(text_id, text) = lore.inlineKey_werwolf_options("Niemanden")
	keyboard.append([InlineKeyboardButton(text, callback_data="werwolf_-1_"+str(text_id)+"_"+str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def inlineKey_anklage(game_id):
	keyboard = []
	for player in game_dict[game_id]["player_list"]:
		(text_id, text) = lore.anklage_options()
		keyboard.append([InlineKeyboardButton(player.name + text, callback_data="anklage_" + str(player.user_id)+"_" + str(text_id) + "_" +str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def inlineKey_abstimmung(game_id):
	keyboard = []
	for player in game_dict[game_id]["anklage_list"]:
		for p in game_dict[game_id]["player_list"]:
			if str(p.user_id) == str(player.user_id):
				(text_id, text) = lore.vote_options()
				keyboard.append([InlineKeyboardButton(p.name + text, callback_data="vote_" + str(player.user_id)+"_" + str(text_id) + "_" +str(game_id))])
				break
	return InlineKeyboardMarkup(keyboard)

def inlineKey_jaeger(p, game_id):
	keyboard = []
	for player in game_dict[game_id]["player_list"]:
		if str(player.user_id) != str(p.user_id) and str(player.user_id) != str(game_dict[game_id]["werwolf_target"]) and str(player.user_id) != str(game_dict[game_id]["hexe_target"]):
			(text_id, text) = lore.inlineKey_jaeger_options()
			keyboard.append([InlineKeyboardButton(player.name + text, callback_data="jaeger_" + str(player.user_id)+"_" + str(text_id) + "_" +str(game_id))])
			#keyboard.append([InlineKeyboardButton(player.name + " erschießen", callback_data="jaeger_" + str(player.user_id)+"_"+str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def inlineKey_seherin(game_id):
	keyboard = []
	for player in game_dict[game_id]["player_list"]:
		if player.role != "Seherin":
			(text_id, text) = lore.seherin_options(player.name)
			keyboard.append([InlineKeyboardButton(text, callback_data="seherin_" + str(player.user_id)+"_" + str(text_id) + "_" +str(game_id))])
			#keyboard.append([InlineKeyboardButton(player.name + " einsehen", callback_data="seherin_" + str(player.user_id)+"_"+str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def inlineKey_hexe_life(game_id):
	keyboard = []
	keyboard.append([InlineKeyboardButton(lore.hexe_save(), callback_data="hexe_life1_"+str(game_id))])
	keyboard.append([InlineKeyboardButton(lore.hexe_let_die(), callback_data="hexe_life0_"+str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def inlineKey_hexe_death(game_id):
	keyboard = []
	for player in game_dict[game_id]["player_list"]:
		keyboard.append([InlineKeyboardButton(player.name + lore.hexe_kill(), callback_data="hexedeath_" + str(player.user_id) + "_" +str(game_id))])
	keyboard.append([InlineKeyboardButton("Niemanden" + lore.hexe_kill(), callback_data="hexedeath_0_" + str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def inlineKey_wolfshund(game_id):
	keyboard = []
	keyboard.append([InlineKeyboardButton(lore.wolfshund_choose_werwolf(), callback_data="wolfshund_werwolf_" +str(game_id))])
	keyboard.append([InlineKeyboardButton(lore.wolfshund_choose_dorf(), callback_data="wolfshund_dorf_" +str(game_id))])
	return InlineKeyboardMarkup(keyboard)

def draw_with_doubles(context, game_id):
	global game_dict
	for p in game_dict[game_id]["player_list"]:
		group = random.random()
		if group < 1/3:
			p.role = "Werwolf"
			context.bot.send_message(chat_id=p.user_id, text=lore.description_werwolf())
		else:
			role = random.random()
			if role < 0.3:
				p.role = "Dorfbewohner"
				context.bot.send_message(chat_id=p.user_id, text=lore.description_dorfbewohner())
			elif role>=0.3 and role < 0.6:
				p.role = "Dorfbewohnerin"
				context.bot.send_message(chat_id=p.user_id, text=lore.description_dorfbewohnerin())
			elif role>=0.6 and role < 0.7:
				p.role = "Rotkäppchen"
				context.bot.send_message(chat_id=p.user_id, text=lore.description_dorfbewohnerin())
			elif role>=0.7 and role < 0.8:
				p.role = "Hexe"
				context.bot.send_message(chat_id=p.user_id, text=lore.description_hexe())
			elif role>=0.8 and role < 0.9:
				p.role = "Seherin"
				context.bot.send_message(chat_id=p.user_id, text=lore.description_seherin())
			else:
				p.role = "Jäger"
				context.bot.send_message(chat_id=p.user_id, text=lore.description_jaeger())
	random.shuffle(game_dict[game_id]["player_list"])

def draw_no_doubles(context, game_id):
	global game_dict
	random.shuffle(game_dict[game_id]["player_list"])
	werwolf_role_list = []
	if len(game_dict[game_id]["player_list"]) >= 6:
		for i in range(0,60):
			werwolf_role_list.append("Werwolf")
		for i in range(0,40):
			werwolf_role_list.append("Wolfshund")
	else:
		for i in range(0,100):
			werwolf_role_list.append("Werwolf")
	
	dorf_role_list = []
	for i in range(0,10):
		dorf_role_list.append("Dorfbewohner")
		dorf_role_list.append("Dorfbewohnerin")
	for i in range(0,20):
		dorf_role_list.append("Jäger")
	for i in range(0,20):
		dorf_role_list.append("Seherin")
	for i in range(0,20):
		dorf_role_list.append("Hexe")
	for i in range(0,20):
		dorf_role_list.append("HarterBursche")

	unique = ["Jäger", "Seherin", "Hexe", "Rotkäppchen", "Wolfshund", "HarterBursche"]

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
		elif p.role == "Dorfbewohner": context.bot.send_message(chat_id=p.user_id, text=lore.description_dorfbewohner())
		elif p.role == "Dorfbewohnerin": context.bot.send_message(chat_id=p.user_id, text=lore.description_dorfbewohnerin())
		elif p.role == "Hexe": context.bot.send_message(chat_id=p.user_id, text=lore.description_hexe())
		elif p.role == "Seherin": context.bot.send_message(chat_id=p.user_id, text=lore.description_seherin())
		elif p.role == "Jäger": context.bot.send_message(chat_id=p.user_id, text=lore.description_jaeger())
		elif p.role == "Rotkäppchen": context.bot.send_message(chat_id=p.user_id, text=lore.description_rotkaeppchen())
		elif p.role == "Wolfshund": context.bot.send_message(chat_id=p.user_id, text=lore.description_wolfshund())
		elif p.role == "HarterBursche": context.bot.send_message(chat_id=p.user_id, text=lore.description_harter_bursche())
	random.shuffle(game_dict[game_id]["player_list"])

def get_fast_game(update, context, game_id):
	status = "aus"
	if game_dict[game_id]["fast_game"]: status="an"	
	context.bot.send_message(chat_id=update.message.chat_id, text="Schnelles Spiel ist " + status)

def toggle_fast_game(update, context, game_id):
	global game_dict
	if game_dict[game_id]["fast_game"]: game_dict[game_id]["fast_game"]=0
	else: game_dict[game_id]["fast_game"] = 1
	get_fast_game(update, context, game_id)

def game_over(context, game_id):
	global game_dict
	if not game_dict[game_id]["game_over_check"]:
		if len(game_dict[game_id]["player_list"]) == 0:
			game_dict[game_id]["admin_id"] = 0
			game_dict[game_id]["running"] = False
			context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=lore.all_dead())
			game_dict[game_id]["game_over_check"] = True
			game_dict[game_id]["state"] = None
			return True
		if not game_dict[game_id]["single_player"]:
			if game_dict[game_id]["player_list"][0].role in werwolf_group: group = werwolf_group
			else: group = dorf_group
			over = True
			for p in game_dict[game_id]["player_list"]:
				if p.role not in group:
					over = False
			if over:
				game_dict[game_id]["admin_id"] = 0
				game_dict[game_id]["running"] = False
				if group == werwolf_group: context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=lore.werwoelfe_win())
				else: context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=lore.dorf_win())
				game_dict[game_id]["game_over_check"] = True
				game_dict[game_id]["state"] = None
				return True
		return False

def wake_werwolf(context, game_id):
	global game_dict
	game_dict[game_id]["game_state"] = "werwolf"
	for p in game_dict[game_id]["player_list"]:
		if p.role in werwolf_group:
			werwolf_tmp_list = []
			for tmp in game_dict[game_id]["player_list"]:
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
			context.bot.send_message(chat_id=p.user_id, text=lore.werwolf_choose_target(), reply_markup=inlineKey_werwolf(game_id))
	while game_dict[game_id]["werwolf_target"] == "0":
			time.sleep(1)
	for player in game_dict[game_id]["player_list"]:
		if str(player.user_id) == str(game_dict[game_id]["werwolf_target"]) and player.role=="Rotkäppchen":
			game_dict[game_id]["werwolf_target"] = "-1"
		if str(player.user_id) == str(game_dict[game_id]["werwolf_target"]) and player.role=="HarterBursche" and game_dict[game_id]["harter_bursche_survive"]:
			game_dict[game_id]["harter_bursche_survive"] = False
			game_dict[game_id]["werwolf_target"] = "-1"
	game_dict[game_id]["game_state"] = "night"

def activate_jaeger(context, p, game_id):
	global game_dict
	game_dict[game_id]["game_state_backup"] = game_dict[game_id]["game_state"]
	game_dict[game_id]["game_state"] = "jaeger"
	context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=p.name + lore.jaeger_reveal())
	context.bot.send_message(chat_id=p.user_id, text=lore.jaeger_choose_target(), reply_markup=inlineKey_jaeger(p, game_id))
	while game_dict[game_id]["game_state"] == "jaeger":
		time.sleep(1)

def wake_seherin(context, game_id):
	global game_dict
	for p in game_dict[game_id]["player_list"]:
		if p.role == "Seherin":
			context.bot.send_message(chat_id=p.user_id, text=lore.seherin_choose_target(), reply_markup=inlineKey_seherin(game_id))
			game_dict[game_id]["game_state"] = "seherin"
	while game_dict[game_id]["game_state"] == "seherin":
		time.sleep(1)

def wake_hexe(context, game_id):
	global game_dict
	if not game_dict[game_id]["hexe_life_juice_used"]:
		victim_name = ""
		for player in game_dict[game_id]["player_list"]:
			if str(player.user_id) == game_dict[game_id]["werwolf_target"]:
				victim_name = player.name
		if victim_name != "":
			for player in game_dict[game_id]["player_list"]:
				if player.role == "Hexe":
					context.bot.send_message(chat_id=player.user_id, text=victim_name + " wurde diese Nacht von den Werwölfen erwischt. Möchtest du diese Person retten?", reply_markup=inlineKey_hexe_life(game_id))
					game_dict[game_id]["game_state"] = "hexe_life"
			while game_dict[game_id]["game_state"] == "hexe_life":
				time.sleep(1)
	if not game_dict[game_id]["hexe_death_juice_used"]:
		print("give death juice")
		for player in game_dict[game_id]["player_list"]:
			if player.role == "Hexe":
				game_dict[game_id]["game_state"] = "hexe_death"
				print("game_state_changed")
				context.bot.send_message(chat_id=player.user_id, text="Willst du noch jemanden töten?", reply_markup=inlineKey_hexe_death(game_id))
		while game_dict[game_id]["game_state"] == "hexe_death":
				time.sleep(1)

def wake_wolfshund(context, game_id):
	global game_dict
	for player in game_dict[game_id]["player_list"]:
		if player.role == "Wolfshund":
			game_dict[game_id]["game_state"] = "wolfshund"
			context.bot.send_message(chat_id=player.user_id, text=lore.wolfshund_options(), reply_markup=inlineKey_wolfshund(game_id))
	while game_dict[game_id]["game_state"] == "wolfshund":
		time.sleep(1)
		print("waiting")


def do_killing(context, game_id):
	global game_dict
	do_killing_list = []
	for p in game_dict[game_id]["player_list"]:
		print(game_dict[game_id]["werwolf_target"])
		print(game_dict[game_id]["hexe_target"])

		if str(p.user_id) == str(game_dict[game_id]["werwolf_target"]) or str(p.user_id) == str(game_dict[game_id]["hexe_target"]):
			print(p.name)
			death_message = lore.death_message()
			context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=p.name + death_message)
			context.bot.send_message(chat_id=p.user_id, text=p.name + death_message)
			if p.role == "Jäger":
				activate_jaeger(context, p, game_id)
			do_killing_list.append(p)
	game_dict[game_id]["werwolf_target"] = ""
	game_dict[game_id]["hexe_target"] = ""
	for kp in do_killing_list:
		game_dict[game_id]["player_list"].remove(kp)

def print_alive(context, game_id):
	message = "Es leben noch: "
	if len(game_dict[game_id]["player_list"]) == 1:
		message = "Es lebt noch: "
	for p in game_dict[game_id]["player_list"]:
		message += p.name + ", "
	context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=message[0:-2])

def prosecute(context, game_id):
	global game_dict
	context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=lore.time_to_prosecute(), reply_markup=inlineKey_anklage(game_id))
	while len(game_dict[game_id]["anklage_list"]) < 3 and len(game_dict[game_id]["anklage_list"]) < len(game_dict[game_id]["player_list"]):
		time.sleep(1)

def vote(context, game_id):
	global game_dict
	kill_list = []
	context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=lore.time_to_vote(), reply_markup=inlineKey_abstimmung(game_id))
	while len(game_dict[game_id]["vote_list"]) < len(game_dict[game_id]["player_list"]):
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
		kill_id = kill_list[0]
		for p in game_dict[game_id]["player_list"]:
			if str(p.user_id) == str(kill_id):
				kill_name = p.name
				kill_player = p
		context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=kill_name + lore.vote_judgement(game_dict[game_id]["vote_options"][str(kill_id)]))
		if kill_player.role == "Jäger":
			activate_jaeger(context, kill_player, game_id)
		game_dict[game_id]["player_list"].remove(kill_player)
	else:
		context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=lore.patt_revote())
		game_dict[game_id]["anklage_list"] = []
		for v in game_dict[game_id]["vote_list"]:
			if v.user_id in kill_list:
				already_in = False
				for a in game_dict[game_id]["anklage_list"]:
					if str(v.user_id) == str(a.user_id):
						already_in = True
				if not already_in:
					#if v not in game_dict[game_id]["anklage_list"]:
					game_dict[game_id]["anklage_list"].append(v)
		game_dict[game_id]["vote_list"] = []
		vote(context, game_id)

def test_chats(context, user_id, name, game_id):
	try:
		context.bot.send_message(chat_id=user_id, text="Herzlich Willkommen bei einem neuen Werwolf-Spiel!")
		return True
	except Unauthorized:
		context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=name + ", bitte beginne einen privaten Chat mit mir!")
		return False

def start_game(context, game_id):
	global game_dict
	game_dict[game_id]["game_over_check"] = False
	if game_dict[game_id]["allow_double_role"]: draw_with_doubles(context, game_id)
	else: draw_no_doubles(context, game_id)
	while not game_over(context, game_id) and not game_dict[game_id]["game_over_check"]:
		game_dict[game_id]["werwolf_target_list"] = []
		game_dict[game_id]["vote_list"] = []
		game_dict[game_id]["anklage_list"] = []
		game_dict[game_id]["game_state"] = "night"
		game_dict[game_id]["werwolf_target"] = "0"
		text_nightfall = lore.nightfall()
		context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=text_nightfall)
		for p in game_dict[game_id]["player_list"]:
			context.bot.send_message(chat_id=p.user_id, text=text_nightfall)
		if game_dict[game_id]["round_number"] == 0:
			wake_wolfshund(context, game_id)
		wake_seherin(context, game_id)
		wake_werwolf(context, game_id)
		wake_hexe(context, game_id)
		do_killing(context, game_id)
		#night is over
		if not game_over(context, game_id):
			print_alive(context, game_id)
			if len(game_dict[game_id]["player_list"])>3:
				game_dict[game_id]["game_state"] = "anklage"
				prosecute(context, game_id)
			else:
				for p in game_dict[game_id]["player_list"]:
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
			for player in game_dict[game_id]["player_list"]:
				if not test_chats(context, player.user_id, player.name, game_id):
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
			#game_dict[game_id].update({"admin_id": 0})
			#game_dict[game_id].update({"running": False})
			#game_dict[game_id].update({"player_list": []})
			#game_dict[game_id].update({"game_over_check": True})

def button_handler_werwolf(update, context):
	global game_dict
	werwolf_list = []
	query = update.callback_query
	game_id = query.data.split("_")[3]
	killing_option = query.data.split("_")[2]
	if not game_dict[game_id]["game_state"] == "werwolf": return
	for p in game_dict[game_id]["player_list"]:
		if p.role in werwolf_group:
			werwolf_list.append(p)
	if query.data.startswith("werwolf_-1"):
		for w in werwolf_list:
			context.bot.send_message(chat_id=w.user_id, text=query.from_user.first_name + " schlägt vor, " + lore.werwolf_response_options(killing_option, "niemanden"))
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
		target_name = ""
		for p in game_dict[game_id]["player_list"]:
			if str(p.user_id) == target_id:
				target_name = p.name
		for w in werwolf_list:
			context.bot.send_message(chat_id=w.user_id, text=query.from_user.first_name + " schlägt vor, " + lore.werwolf_response_options(killing_option, target_name))
	if len(werwolf_list) == len(game_dict[game_id]["werwolf_target_list"]) and len(werwolf_list) != 0:
		same = True
		first_target = game_dict[game_id]["werwolf_target_list"][0]
		for t in game_dict[game_id]["werwolf_target_list"]:
			if not t.target_id == first_target.target_id:
				same = False
				break
		if same:
			game_dict[game_id]["werwolf_target"] = first_target.target_id
			if game_dict[game_id]["werwolf_target"] == "-1": target_name = "niemanden"
			for w in werwolf_list:
				context.bot.send_message(chat_id=w.user_id, text="Die Werwölfe haben beschlossen, " + lore.werwolf_response_options(killing_option, target_name))

def button_handler_anklage(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[3]
	anklage_option = query.data.split("_")[2]
	if not game_dict[game_id]["game_state"] == "anklage": return
	for p in game_dict[game_id]["player_list"]:
		if str(p.user_id) == str(query.from_user.id):
			anklage_id = query.data.split("_")[1]
			anklage_in_list = False
			for a in game_dict[game_id]["anklage_list"]:
				if str(a.user_id) == anklage_id: anklage_in_list = True
			anklaeger_name = ""
			for py in game_dict[game_id]["player_list"]:
				if str(py.user_id) == str(query.from_user.id):
					anklaeger_name = py.name
					break
			angeklagter_name = ""
			for py in game_dict[game_id]["player_list"]:
				if str(py.user_id) == anklage_id:
					angeklagter_name = py.name
					break
			if not anklage_in_list:
				anklaeger_in_list = False
				for a in game_dict[game_id]["anklage_list"]:
					if str(a.by_id) == str(query.from_user.id):
						a.user_id = anklage_id
						anklaeger_in_list = True
						context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=anklaeger_name + lore.anklage_change(anklage_option, angeklagter_name))
						break
				if not anklaeger_in_list:
					game_dict[game_id]["anklage_list"].append(Prosecuted(anklage_id, query.from_user.id))
					context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=anklaeger_name + lore.anklage_new(anklage_option, angeklagter_name))
			break

def button_handler_vote(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[3]
	vote_option = query.data.split("_")[2]
	if not game_dict[game_id]["game_state"] == "vote": return
	user_allowed = False
	for p in game_dict[game_id]["player_list"]:
		if str(p.user_id) == str(query.from_user.id):
			vote_id = query.data.split("_")[1]
			already_voted = False
			voter_name = ""
			for pl in game_dict[game_id]["player_list"]:
				if str(pl.user_id) == str(query.from_user.id):
					voter_name = pl.name
					break
			voted_name = ""
			for py in game_dict[game_id]["player_list"]:
				if str(py.user_id) == str(vote_id):
					voted_name = py.name
					game_dict[game_id]["vote_options"].update({str(vote_id):vote_option})
					break
			for v in game_dict[game_id]["vote_list"]:
				if str(v.by_id) == str(query.from_user.id):
					already_voted = True
					v.user_id = vote_id
					context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=voter_name + lore.vote_change(vote_option, voted_name))
					game_dict[game_id]["last_vote_option"] = vote_option
					break
			if not already_voted:
				game_dict[game_id]["vote_list"].append(Prosecuted(vote_id, query.from_user.id))
				context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=voter_name + lore.vote_new(vote_option, voted_name))
				game_dict[game_id]["last_vote_option"] = vote_option
			break

def button_handler_jaeger(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[3]
	if not game_dict[game_id]["game_state"] == "jaeger": return
	kill_option = query.data.split("_")[2]
	kill_id = query.data.split("_")[1]
	kill_name = ""
	for pl in game_dict[game_id]["player_list"]:
		if str(pl.user_id) == str(kill_id):
			kill_name = pl.name
			game_dict[game_id]["player_list"].remove(pl)
			break 
	context.bot.send_message(chat_id=game_dict[game_id]["game_chat_id"], text=kill_name + lore.jaeger_shot(kill_option))
	game_dict[game_id]["game_state"] = game_dict[game_id]["game_state_backup"]
	game_dict[game_id]["game_state_backup"] = None

def button_handler_seherin(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[3]
	seherin_option = query.data.split("_")[2]
	watch_id = query.data.split("_")[1]
	if game_dict[game_id]["game_state"] != "seherin": return
	watch_in_list = False
	seherin_id = ""
	for player in game_dict[game_id]["player_list"]:
		print(player.role)
		if player.role == "Seherin":
			print(player.user_id)
			seherin_id = str(player.user_id)
	for player in game_dict[game_id]["player_list"]:
		if str(player.user_id) == watch_id:
			if player.role in werwolf_group:
				context.bot.send_message(chat_id=seherin_id, text=lore.seherin_werwolf(seherin_option, player.name))
			else:
				context.bot.send_message(chat_id=seherin_id, text=lore.seherin_no_werwolf(seherin_option, player.name))
			game_dict[game_id]["game_state"] = "night"

def button_handler_hexe_life(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[2]
	if game_dict[game_id]["game_state"] != "hexe_life": return
	if query.data.startswith("hexe_life0_"):
		game_dict[game_id]["game_state"] = "night"
	elif query.data.startswith("hexe_life1_"):
		game_dict[game_id]["hexe_life_juice_used"] = True
		game_dict[game_id]["werwolf_target"] = 0
		game_dict[game_id]["game_state"] = "night"

def button_handler_hexe_death(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[2]
	if game_dict[game_id]["game_state"] != "hexe_death": return
	if query.data.startswith("hexedeath_0_"):
		game_dict[game_id]["game_state"] = "night"
		return
	elif query.data.startswith("hexedeath_"):
		hexe_target_id = query.data.split("_")[1]
		game_dict[game_id]["hexe_target"] = hexe_target_id
		game_dict[game_id]["hexe_death_juice_used"] = True
		game_dict[game_id]["game_state"] = "night"

def button_handler_wolfshund_choose(update, context):
	global game_dict
	query = update.callback_query
	game_id = query.data.split("_")[2]
	if not game_dict[game_id]["game_state"] == "wolfshund": return
	target = query.data.split("_")[1]
	if target == "werwolf":
		print("choose werwolf")
		for player in game_dict[game_id]["player_list"]:
			print(player.role)
			if player.role == "Wolfshund":
				print(player.name)
				player.role = "Werwolf"
	elif target == "dorf":
		print("choose dorf")
		for player in game_dict[game_id]["player_list"]:
			print(player.role)
			if player.role == "Wolfshund":
				print(player.name)
				player.role = "Dorfbewohner"
	game_dict[game_id]["game_state"] = "night"

def button_handler(update, context):
	if update.callback_query.data.startswith("menu_"):
		button_handler_menu(update, context)
	elif update.callback_query.data.startswith("werwolf_"):
		button_handler_werwolf(update, context)
	elif update.callback_query.data.startswith("anklage_"):
		button_handler_anklage(update, context)
	elif update.callback_query.data.startswith("vote_"):
		button_handler_vote(update, context)
	elif update.callback_query.data.startswith("jaeger_"):
		button_handler_jaeger(update, context)
	elif update.callback_query.data.startswith("seherin_"):
		button_handler_seherin(update, context)
	elif update.callback_query.data.startswith("hexe_life"):
		button_handler_hexe_life(update, context)
	elif update.callback_query.data.startswith("hexedeath_"):
		button_handler_hexe_death(update, context)
	elif update.callback_query.data.startswith("wolfshund_"):
		button_handler_wolfshund_choose(update, context)

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
	context.bot.send_message(chat_id=update.message.chat_id, text="Herzlich Wilkommen beim WerWolfBot!")

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