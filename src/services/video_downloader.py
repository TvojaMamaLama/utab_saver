from pytube import YouTube

from services.base import BaseService


class VideoDownloader(BaseService):
    def __init__(self, link: str):
        self.link = link

    def act(self):
        downloader = YouTube(self.link)
        video = downloader.streams.filter(res='720p', file_extension='mp4').first()
        video_path = video.download('media')
        return video_path
