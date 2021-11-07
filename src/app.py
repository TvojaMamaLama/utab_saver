import os

from telebot import TeleBot
from telebot.types import Message

from config import BOT_TOKEN
from services.video_downloader import VideoDownloader


bot = TeleBot(token=BOT_TOKEN)


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


bot.infinity_polling()
