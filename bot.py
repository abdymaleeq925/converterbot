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
    try:
        VID_ID = ''
        VID_ID = validation.to_valid(url, VID_ID)
        doc = VID_ID
        bot.send_message(message.chat.id, "File is downloading..")
        download.worker(VID_ID)
    except Exception as e:
        bot.send_message(message.chat.id, f"Something is wrong! Error '{e}'")

    
    keyboard = types.InlineKeyboardMarkup()
    mp3 = types.InlineKeyboardButton(text="MP3", callback_data="mp3")
    mp4 = types.InlineKeyboardButton(text="MP4", callback_data="mp4")
    keyboard.add(mp3, mp4)
    bot.send_message(message.chat.id, "Choose format you want to get:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    if call.data == 'mp3':
        print(doc)
        mp4 = base_dir + doc + '.mp4'
        mp3 = base_dir + doc + '.mp3'
        cmd = "ffmpeg -i {} -vn {}".format(mp4, mp3)
        os.system(cmd)
        os.system("afplay {}".format(mp3))
        aud = open(f"{doc}.mp3", 'rb')
        bot.send_audio(call.message.chat.id, aud)
        os.remove(f"{doc}.mp3")
    elif call.data == 'mp4':
        vid = open(f"{doc}.mp4", 'rb')
        bot.send_video(call.message.chat.id, vid)
        bot.send_message(call.message.chat.id, "Thank you!")
        os.remove(f"{doc}.mp4")  
        
bot.infinity_polling()