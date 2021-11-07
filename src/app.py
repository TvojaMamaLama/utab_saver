import os

from flask import Flask
from flask import request
from telebot import TeleBot
from telebot.types import Message
from telebot.types import Update

from config import BOT_TOKEN
from config import HEROKU_HOST
from config import PORT
from services.video_downloader import VideoDownloader


bot = TeleBot(token=BOT_TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    bot.reply_to(message, "Привет, я качаю видосы с ютуба, кидай ссылку :)")


@bot.message_handler()
def send_video(message: Message):
    video_downloader = VideoDownloader(message.text)
    video_path: str = video_downloader()

    with open(video_path, 'rb') as video:
        bot.send_document(
            chat_id=message.chat.id,
            data=video,
            timeout=100,
        )

    os.remove(video_path)


@server.route('/handler', methods=['POST'])
def get_telegram_message():
    json_string = request.get_data().decode('utf-8')
    update = Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def set_bot_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'{HEROKU_HOST}/handler')
    return "!", 200


server.run(host="0.0.0.0", port=PORT)
