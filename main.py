from revChatGPT.V3 import Chatbot
from random import randint
import telebot
import datetime


bot = telebot.TeleBot("6206728258:AAGBhCLfGmDfwTy-pD5P4_SyRIRkY6_Cfss")
chatbot = Chatbot(api_key="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")

firstMemePromt = "Ответь на сообщение {} в стиле оксимирона, без своих комментариев (это очень важно), сообщение на русском, уточни, что ты оксимирон, и скажи дату"
secondMemePromt = "Ответь на сообщение {} строчкой из песни оксимирона, не забудь уточнить, что это сказал оксимирон, и название песни"

last_message_time = None


def MemePromt(message):
    if randint(0,1) == 0:
        answer = chatbot.ask(firstMemePromt.format(message))
        return answer
    else:
        answer = chatbot.ask(secondMemePromt.format(message))
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


# @bot.message_handler(commands=['settings'])
# def NumOfPromt(message):
#     if message.chat.type == 'private' and message.chat.username == "kobay9iq":
#         bot.send_message(message.chat.id, 
#                         f'''Текущий первый промт:\n
#                         {firstMemePromt}. \n
#                         Текущий второй промт: \n
#                         {secondMemePromt}.'''
#                         )
#         bot.send_message(message.chat.id, "Какой промт хотите поменять?")
#         bot.register_next_step_handler(message, ChangingPromt)

# def ChangingPromt(message):
#     bot.send_message(message.chat.id, '''Какой будет новый промт?\n 
#                     Не забудь добавить {} на месте сообщения юзера''')
#     if message.text == "1":
#         bot.register_next_step_handler(message, ChangingFirtstPromt)
#     elif message.text == "2":
#         bot.register_next_step_handler(message, ChangingSecondPromt)
#     else:
#         bot.send_message(message.chat.id, "Неверное число (или это не число?)")
#         return

# def ChangingFirtstPromt(message):
#     firstMemePromt = message.text
#     bot.send_message(message.chat.id, "Успешно!")
    
# def ChangingSecondPromt(message):
#     secondMemePromt = message.text
#     bot.send_message(message.chat.id, "Успешно!")


@bot.message_handler(content_types=['text'])
def MemeReply(message):
    global last_message_time
    if len(message.text) >= 5 and not(message.text.startswith('/')):
        if (last_message_time is None or datetime.datetime.now() > last_message_time + datetime.timedelta(seconds=300)):
            bot.reply_to(message, MemePromt(message.text))
            last_message_time = datetime.datetime.now()
        elif message.text.startswith('$'):
            bot.reply_to(message, MemePromt(message.text))
            

print("STARTED")            
bot.infinity_polling()