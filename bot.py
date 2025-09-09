#!/usr/bin/python

# This is a simple bot with schedule timer
# https://schedule.readthedocs.io

import time, threading, schedule, random, math
from telebot import TeleBot

API_TOKEN = ''
bot = TeleBot(API_TOKEN)
balance = 0 

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! ")

@bot.message_handler(commands=['help']) #хелп
def send_help(message):
    bot.reply_to(message, "/set -таймер \n /unset - выкоючить таймер \n /heh - пишет hehe \n /poll - квиз \n /random - рандомайзер чисел, напиши диапазон через пробел \n /plus, /minus, /divide, /multi - калькулятор напиши 2 числа через пробел и бот сложит/вычтет/разделит/умножит эти 2 числа \n /round - округлит число, напиши дробь и через пробел скольо чисел должно остаться после запитой \n /game - простая игра напиши от одного до пяти чтобы угадать где монета \n /balance - твой баланс ")

def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='Beep!')


@bot.message_handler(commands=['set']) # включить таймер
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
    else:
        bot.reply_to(message, 'Usage: /set <seconds>')


@bot.message_handler(commands=['unset']) #выключить таймер
def unset_timer(message):
    schedule.clear(message.chat.id)

@bot.message_handler(commands=['heh'])
def send_heh(message):
    count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    bot.reply_to(message, "he" * count_heh)
    
@bot.message_handler(commands=["poll"]) #квиз
def create_poll(message):
    bot.send_message(message.chat.id, "English Article Test")
    answer_options = ["a", "an", "the", "-"]

    bot.send_poll(
        chat_id=message.chat.id,
        question="We are going to '' park.",
        options=answer_options,
        type="quiz",
        correct_option_id=2,
        is_anonymous=False,
    )

@bot.poll_answer_handler()
def handle_poll(poll):
    pass

@bot.message_handler(commands=['random']) #рандомайзер чисел
def send_random(message):
    rmsg = message.text.split()
    rnumber = random.randint(int(rmsg[1]), int(rmsg[2]))
    bot.reply_to(message, rnumber)

@bot.message_handler(commands=['plus']) # сложение
def send_plus(message):
    smsg = message.text.split()
    snumber = int(smsg[1]) + int(smsg[2])
    bot.reply_to(message, snumber)

@bot.message_handler(commands=['minus']) # вычетание
def send_minus(message):
    vmsg = message.text.split()
    vnumber = int(smsg[1]) - int(smsg[2])
    bot.reply_to(message, vnumber)

@bot.message_handler(commands=['divide']) #диление 
def send_divide(message):
    dmsg = message.text.split()
    dnumber = int(dmsg[1]) / int(dmsg[2])
    bot.reply_to(message,dnumber)

@bot.message_handler(commands=['multi']) #умножение
def send_multi(message):
    mmsg = message.text.split()
    mnumber = int(mmsg[1]) * int(mmsg[2])
    bot.reply_to(message, mnumber)

@bot.message_handler(commands=['round']) #округление
def send_round(message):
    mmsg = message.text.split()
    mnumber = round(float(mmsg[1]), int(mmsg[2]))
    bot.reply_to(message, mnumber)

@bot.message_handler(commands=['game']) #игра
def send_game(message):
    global balance
    pick1 = message.text.split()
    pick = int(pick1[1])
    coin = random.randint(1, 5)
    if pick == coin:
        bot.reply_to(message, "молодец, ты угадал")
        balance += 1
    else:
        bot.reply_to(message, "увы, но ты проиграл :(")

@bot.message_handler(commands=['balance']) #баланс
def send_balance(message):
    global balance
    bot.reply_to(message, balance)

if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
