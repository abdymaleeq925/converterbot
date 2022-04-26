import telebot
from telebot import types
import validation
import os
import download
from config import TOKEN


bot = telebot.TeleBot(TOKEN)
doc = ''
base_dir = "/home/abdymalik/Desktop/telegrambot/"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """
    Welcome to File Converter. 
Please send the link for downloading. 
Have a nice day!
    """)

@bot.message_handler()
def download_file(message):
    url = message.text
    
    keyboard = types.InlineKeyboardMarkup()
    mp3 = types.InlineKeyboardButton(text="MP3", callback_data=f"{url}-mp3")
    mp4 = types.InlineKeyboardButton(text="MP4", callback_data=f"{url}-mp4")
    keyboard.add(mp3, mp4)
    bot.send_message(message.chat.id, "Choose format you want to get:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    message = call.message
    doc = str(call.data).split('-')
    url_name = doc[0]
    format = doc[1]
    if format == 'mp3':
        try:
            VID_ID = ''
            VID_ID = validation.to_valid(url_name, VID_ID)
            bot.send_message(message.chat.id, "File is downloading..")
            download.worker(VID_ID)
        except Exception as e:
            bot.send_message(message.chat.id, f"Something is wrong! Error '{e}'")

        mp4 = base_dir + VID_ID + '.mp4'
        mp3 = base_dir + VID_ID + '.mp3'
        cmd = "ffmpeg -i {} -vn {}".format(mp4, mp3)
        os.system(cmd)
        os.system("afplay {}".format(mp3))
        aud = open(f"{VID_ID}.mp3", 'rb')
        bot.send_audio(message.chat.id, aud)
        bot.send_message(message.chat.id, "Enjoy your file! Have a nice day!")
        os.remove(f"{VID_ID}.mp3")
        os.remove(f"{VID_ID}.mp4")

    elif format == 'mp4':
        try:
            VID_ID = ''
            VID_ID = validation.to_valid(url_name, VID_ID)
            bot.send_message(message.chat.id, "File is downloading..")
            download.worker(VID_ID)
        except Exception as e:
            bot.send_message(message.chat.id, f"Something is wrong! Error '{e}'")

        vid = open(f"{VID_ID}.mp4", 'rb')
        bot.send_video(message.chat.id, vid)
        bot.send_message(message.chat.id, "Enjoy your file! Have a nice day!")
        os.remove(f"{VID_ID}.mp4")  
        
bot.infinity_polling()