import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('YT_API_KEY')

    @classmethod
    def get_service(cls):
        """класс-метод, возвращающий объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=cls.api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel_dict = (
            self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute())
        self.title = self.channel_dict['items'][0]['snippet']['title']
        self.description = self.channel_dict['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriberCount = self.channel_dict['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel_dict['items'][0]['statistics']['videoCount']
        self.view_count = self.channel_dict['items'][0]['statistics']['viewCount']

    def __str__(self):
        """отображение информации об объекте класса для пользователей"""
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """сложение количества подписчиков"""
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other):
        """вычитание количества подписчиков"""
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __lt__(self, other):
        """сравнение (меньше) количества подписчиков"""
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __le__(self, other):
        """сравнение (меньше или равно) количества подписчиков"""
        return int(self.subscriberCount) <= int(other.subscriberCount)

    def __gt__(self, other):
        """сравнение (больше) количества подписчиков"""
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __ge__(self, other):
        """сравнение (больше или равно) количества подписчиков"""
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def __eq__(self, other):
        """сравнение (равно) количества подписчиков"""
        return int(self.subscriberCount) == int(other.subscriberCount)

    @property
    def get_channel_id(self):
        """Геттер для channel_id"""
        return self.__channel_id

    def to_json(self, filename):
        """метод, сохраняющий в файл значения атрибутов экземпляра `Channel`"""
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.channel_dict, file, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel_dict, indent=2, ensure_ascii=False))
