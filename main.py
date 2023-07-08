from revChatGPT.V3 import Chatbot
from pictures import Picture
from telebot import types
import telebot, configparser, datetime

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

bot = telebot.TeleBot(token = config["BOT API Key"]["bot_key"])
chatbot = Chatbot(api_key = config["OpenAI API Key"]["gpt_key"])

helpText = "/promt - запрос к ChatGPT без всяких оксимиронов \
и прочих приколов.\
\n/reset - сброс промтов к значениям по умолчанию.\
\n/settings - установка новых промтов.\
\n/currentPromts - текущие промты.\
\n\nИспользуя \"$\" перед *вашим* сообщением, \
вы вызовите промт ручного вызова \
и получите ответ от бота на *ваше* сообщение.\
\n\nИспользуя команду \"!гпт\" при ответе на чужое сообщение, вы вызовите \
промт ручного вызова и получите ответ от бота на сообщение, \
*на которое вы отвечали.*"

defaultManualMemePromt = "Ответь на сообщение {} в стиле оксимирона,\
без своих комментариев (это очень важно), сообщение на русском, уточни,\
что ты оксимирон, и скажи дату"
defaultRandomMemePromt = "Ответь на сообщение {} строчкой из песни оксимирона,\
не забудь уточнить, что это сказал оксимирон, и название песни"

picturesEnabled = True

lastMessageTime = None
botCoolDownInSec = 300

manualMemePromt = defaultManualMemePromt
randomMemePromt = defaultRandomMemePromt


def MemePromtHandler(message, random):
    if len(message.text) >= 5 and not (message.text.startswith('/')) and random:
        if picturesEnabled:
            SendMessageWithPicture(message, manual = False)
        else:
            bot.reply_to(message, MemePromt(message.text, manual=False))
    
    elif message.text.startswith('$'):
        if picturesEnabled:
                SendMessageWithPicture(message, manual = True)
        else:
            bot.reply_to(message, MemePromt(message.text, manual=True))
    
    elif message.reply_to_message and message.text.startswith('!гпт'):
        second_person_message = message.reply_to_message
        if picturesEnabled:
            SendMessageWithPicture(message, manual = True)
        else:
            bot.reply_to(second_person_message, 
                     MemePromt(second_person_message.text, manual=True))
            

def SendMessageWithPicture(message, manual):
    picture = open(Picture(), "rb")
    if picture is None: return
    
    bot.send_photo(message.chat.id, picture, 
                   caption = MemePromt(message.text, manual = manual),
                   reply_to_message_id = message.id)
    

def MemePromt(message, manual):
    if manual:
        answer = chatbot.ask(manualMemePromt.format(message))
        return answer
    else:
        answer = chatbot.ask(randomMemePromt.format(message))
        return answer


@bot.message_handler(commands=['gpt'])
def Help(message):
    bot.send_message(message.chat.id, helpText,
                     parse_mode = "Markdown")
    

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
def PromtsSettings(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Рандом промт", callback_data="1")
    button2 = types.InlineKeyboardButton("Промт ручного вызова", callback_data="2")
    markup.add(button1, button2)

    bot.send_message(message.chat.id, f'Какой промт вы хотите поменять?\n\
*Текущий рандом-промт:*\n\
{randomMemePromt}.\n*Текущий промт ручного вызова:*\n{manualMemePromt}.',
                    parse_mode = "Markdown", reply_markup = markup)


@bot.callback_query_handler(func=lambda call: True)
def SettingButtonPressed(call):
    bot_msg = bot.reply_to(call.message, 
                           f"""Ответьте на мое сообщение новым промтом,
вставьте {{}} туда, *где должно находится сообщение от пользователя* \n 
*Пример:*\n{defaultManualMemePromt}""", parse_mode = "Markdown")
    
    bot.register_for_reply_by_message_id(bot_msg.id, 
                                lambda  message: ChangingPromts(message, call)
                                        )


def ChangingPromts(message, call):
    if call.data == "1" and "{}" in message.text:
        global randomMemePromt
        randomMemePromt = message.text
        
        bot.reply_to(message, "Рандом-промт успешно изменен!")
        CurrentPromts(message)
    elif call.data == "2" and "{}" in message.text:
        global manualMemePromt
        manualMemePromt = message.text
        
        bot.reply_to(message, "Промт ручного вызова успешно изменен!")
        CurrentPromts(message)
    else:
        bot.send_message(message.chat.id, 
                         "Ваше сообщение не содержит в себе {}.")


@bot.message_handler(commands=['currentPromts'])
def CurrentPromts(message):
    bot.send_message(message.chat.id, f"*Рандом-пронт:* {randomMemePromt}\n\
*Промт ручного вызова:* {manualMemePromt}", parse_mode="Markdown")


@bot.message_handler(commands=["reset"])
def BackPromtsToDefault(message):
    global manualMemePromt
    global randomMemePromt
    manualMemePromt = defaultManualMemePromt
    randomMemePromt = defaultRandomMemePromt
    
    bot.reply_to(message, "Промты возращены к значениям по умолчанию")
    CurrentPromts(message)


@bot.message_handler(content_types=['text'])
def MemeReply(message):
    global lastMessageTime
    if (lastMessageTime is None or (datetime.datetime.now() >
        lastMessageTime + datetime.timedelta(seconds=botCoolDownInSec))):
            MemePromtHandler(message, random=True)
            lastMessageTime = datetime.datetime.now()
    else: 
        MemePromtHandler(message, random=False)


print("STARTED")
bot.infinity_polling()
