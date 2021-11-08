from pytube import YouTube
from telebot import TeleBot
from telebot.types import Message

from services.base import BaseService


class VideoDownloader(BaseService):
    def __init__(self, bot: TeleBot, message: Message):
        self.bot = bot
        self.message = message
        self.link = message.text

    def act(self):
        self.bot.send_message(self.message.chat.id, 'Начали скачивать...')
        downloader = YouTube(self.link)
        video = downloader.streams.filter(res='720p', file_extension='mp4').first()
        video_path = video.download('media')
        self.bot.send_message(self.message.chat.id, 'Скачали...')
        return video_path
