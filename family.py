import json
import codecs
import telebot
from telebot import types
from collections import deque
import time

bot = telebot.TeleBot('1292670422:AAFotKwnBq4Cs31rH98k58rhC0qcNWkqD50')

json_file = codecs.open('botic.json', 'r', 'utf_8_sig')
botic = json.load(json_file)["themes"]
json_file.close()

wait = deque()

names = []
for a in botic:
    theme = botic[a]["name"]
    names.append(theme)

themes_rus = []
themes_en = []

for key in botic:
    themes_en = list(botic.keys())
    themes_rus.append(botic[key]["name"])

selection_family = themes_en[0]

word_family = []
transcription_family = []
translation_family = []

word_family = botic[selection_family]["word"]
transcription_family = botic[selection_family]["transcription"]
translation_family = botic[selection_family]["translation"]


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, text="Привет, сегодня мы с тобой выучим новые слова.")
    keyboard = types.InlineKeyboardMarkup()
    for i in range(4):
        z = types.InlineKeyboardButton(text=names[i], callback_data=names[i])
        keyboard.add(z)
    bot.send_message(message.from_user.id, text='Выбери тему, которую ты хочешь изучить.', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.from_user.id, "Напиши \"/start\"")


@bot.message_handler(content_types=['text'])
def get_in_message(message):
    into = message.text
    wait.append(into)
    print(wait)


def get_out_message():
    while len(wait) == 0:
        time.sleep(1)
    out = wait.popleft()
    return out


def get_messages(message):
    wait_message = get_out_message()
    for i in range(31):
        if wait_message == word_family[i]:
            bot.send_message(message.from_user.id,
                             text=word_family[i] + "  ⟶  " + transcription_family[i] + "  ⟶  " + translation_family[i])


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'Семья':
        bot.send_message(call.message.chat.id, text="Отличный выбор! Давай посмотрим, какие слова нам предстоит "
                                                    "выучить по теме \"Семья\"." + "\n\n" +
                                                    botic["family"]["list"])
        bot.send_message(call.message.chat.id,
                         text="Если ты сомневаешься в произношении какого-либо слова, можешь написать мне русский"
                              " вариант этого слова, и я пришлю тебе его транскрипцию.")
        bot.send_message(call.message.chat.id,
                         text="Когда ты будешь уверен в том, что выучил все слова, нажимай на кнопку, и мы проверим, "
                              "насколько хорошо ты их знаешь.",
                         reply_markup=keyboard_ready)

    if call.data == 'ready':
        bot.send_message(call.message.chat.id, text="Отлично! Тогда приступим. Я тебе пишу слово, а ты мне его перевод.")
        for x in range(len(botic["family"]["word"])):
            bot.send_message(call.message.chat.id, text=botic["family"]["word"][x])
            wait_message = get_out_message()
            if wait_message == botic["family"]["translation"][x]:
                bot.send_message(call.message.chat.id, text="Супер!")
            else:
                while wait_message != botic["family"]["translation"][x]:
                    bot.send_message(call.message.chat.id,
                                     text="Неверно. Попробуй ещё раз." + "\n\n" + botic["family"]["word"][x])
                    wait_message = get_out_message()
                    bot.send_message(call.message.chat.id, text="Супер!")
        end = types.InlineKeyboardMarkup()
        key_end = types.InlineKeyboardButton(text='Вернуться к спискам тем', callback_data='end')
        end.add(key_end)
        bot.send_message(call.message.chat.id, text="Отлично! Ты выучил все слова по теме \"Семья\". В честь этого дарю тебе свой любимый стикер:", reply_markup=end)
        bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAIE517FXQtjreaMPb0Ry4tvV_ChlriEAALHAgACusCVBRXK57i_4oRFGQQ')

    if call.data == 'end':
        keyboard = types.InlineKeyboardMarkup()
        for i in range(4):
            z = types.InlineKeyboardButton(text=names[i], callback_data=names[i])
            keyboard.add(z)
        bot.send_message(call.message.from_user.id, text='Выбери тему, которую ты хочешь изучить.', reply_markup=keyboard)


keyboard_ready = types.InlineKeyboardMarkup()
key_ready = types.InlineKeyboardButton(text='Я выучил слова!', callback_data='ready')
keyboard_ready.add(key_ready)


bot.polling(none_stop=True, interval=0)
