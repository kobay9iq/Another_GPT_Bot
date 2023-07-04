from revChatGPT.V3 import Chatbot
import telebot
from telebot import types
import config
import datetime


bot = telebot.TeleBot("6206728258:AAGBhCLfGmDfwTy-pD5P4_SyRIRkY6_Cfss")
chatbot = Chatbot(
    api_key="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")

defaultManualMemePromt = "Ответь на сообщение {} в стиле оксимирона, без своих\
комментариев (это очень важно), сообщение на русском, уточни,\
что ты оксимирон, и скажи дату"
defaultRandomMemePromt = "Ответь на сообщение {} строчкой из песни оксимирона,\
не забудь уточнить, что это сказал оксимирон, и название песни"

last_message_time = None

manualMemePromt = defaultManualMemePromt
randomMemePromt = defaultRandomMemePromt


def MemePromt(message, manual):
    if manual:
        answer = chatbot.ask(manualMemePromt.format(message))
        return answer
    else:
        answer = chatbot.ask(randomMemePromt.format(message))
        return answer


@bot.message_handler(commands=['promt'])
def Promt(message):
    message_text = message.text.replace('/promt', '')
    if len(message_text) != 0:
        bot.reply_to(message, chatbot.ask(message_text))
    else:
        bot.reply_to(message, chatbot.ask("Кто ты?"))


@bot.message_handler(commands=['reset'])
def Reset(message):
    chatbot.reset()
    bot.reply_to(message, "Успешный сброс!")


@bot.message_handler(commands=['settings'])
def NumOfPromt(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Рандом промт")
    button2 = types.KeyboardButton("Промт ручного вызова")
    markup.add(button1, button2)

    bot.send_message(message.chat.id, f'*Текущий рандом-промт:*\n\
{randomMemePromt}.\n*Текущий промт ручного вызова:*\n\
{manualMemePromt}.', parse_mode="Markdown", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def SettingButtonPressed(call):
    print("1")
    if call.data == "Рандом промт":
        print("2")
        bot.send_message(call.message.chat.id, "1")
    

@bot.message_handler(commands=['currentPromts'])
def CurrentPromts(message):
    bot.send_message(message.chat.id, f"*Рандом-пронт:* {manualMemePromt}\n\
*Промт ручного вызова:* {randomMemePromt}", parse_mode="Markdown")


@bot.message_handler(commands=["default"])
def BackPromtsToDefault(message):
    global manualMemePromt
    global randomMemePromt
    manualMemePromt = defaultManualMemePromt
    randomMemePromt = defaultRandomMemePromt
    
    bot.reply_to(message, "Промты возращены к значениям по умолчанию")
    CurrentPromts(message)

@bot.message_handler(content_types=['text'])
def MemeReply(message):
    global last_message_time
    if len(message.text) >= 5 and not (message.text.startswith('/')):
        if (last_message_time is None 
            or (datetime.datetime.now() >
            last_message_time + datetime.timedelta(seconds=300))):
                bot.reply_to(message, MemePromt(message.text, manual=False))
                last_message_time = datetime.datetime.now()
        elif message.text.startswith('$'):
            bot.reply_to(message, MemePromt(message.text, manual=True))


print("STARTED")
bot.infinity_polling()
