import telebot
import weatherapp.weather
import config
import time

print(weatherapp.weather.weather_context)


bot = telebot.TeleBot(config.TOKEN)

message_ids = {}


def send_murkup(chat_id, message_id):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text="погода", callback_data="weather"))
    markup.add(telebot.types.InlineKeyboardButton(text="twich", callback_data="twitch"))
    markup.add(telebot.types.InlineKeyboardButton(text="clear chat", callback_data="clearchat"))

    bot.send_message(chat_id, text="че как", reply_markup=markup)

    bot.delete_message(chat_id, message_id)



def create_back_button(chat_id):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text="back", callback_data="back"))
    if weatherapp.weather.weather_context:
        text = "enter city"
    bot.send_message(chat_id, text=text, reply_markup=markup)



# COMMAND HANDLERS
@bot.message_handler(commands=["start"])
def start_message(message):
    send_murkup(message.chat.id, message.message_id)


# MESSAGE TEXT HANDLERS
@bot.message_handler(content_types=["text"])
def text_hand(message):
    # print(weather.weather_context)
    chat_id = message.chat.id
    message_id = message.message_id

    if chat_id not in message_ids.keys():
        message_ids[chat_id] = []        
    message_ids[chat_id].append(message_id)

    if weatherapp.weather.weather_context :
        data = weatherapp.weather.weather_parse(message.text)        
        if data != None:
            bot.delete_message(chat_id, message_id-1)
            bot.send_message(chat_id, text=data)
            create_back_button(chat_id)
        else:
            bot.delete_message(chat_id, message_id-1)
            bot.send_message(chat_id, text="city not found")
            create_back_button(message.chat.id) 

        message_ids[chat_id].append(message_id+1)
     
    print(message_ids) 

# CALLBACK HANDLERS
@bot.callback_query_handler(func=lambda call: call.data == "back")
def back_hand(call):
    send_murkup(call.message.chat.id, call.message.message_id)
    weatherapp.weather.weather_context = False


@bot.callback_query_handler(func=lambda call: call.data == "weather")
def weather_hand(call):
    weatherapp.weather.weather_context = True
    bot.delete_message(call.message.chat.id, call.message.message_id)
    create_back_button(call.message.chat.id)

    # print(weather.weather_context)



@bot.callback_query_handler(func=lambda call: call.data == "clearchat")
def clear_chat_hand(call): 
    global message_ids
    chat_id = call.message.chat.id

    for mid in message_ids[chat_id]:
        bot.delete_message(chat_id, mid)
    del message_ids[chat_id]
        # try:
        #     bot.delete_message(call.message.chat.id, mi)
        # except:
        #     time.sleep(2)
        #     bot.delete_message(call.message.chat.id, mi)


   




bot.infinity_polling()