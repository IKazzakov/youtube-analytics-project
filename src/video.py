from src.channel import Channel


class Video(Channel):
    """Класс для видео с Ютуб канала. Наследуется от класса Channel"""

    def __init__(self, video_id):
        """Экземпляр инициализируется по id видео. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        try:
            self.video_response = self.get_service().videos().list(
                part='snippet,statistics,contentDetails,topicDetails',
                id=video_id
                ).execute()
            self.title: str = self.video_response['items'][0]['snippet']['title']
            self.video_url = f'https://www.youtube.com/video/{self.video_id}'
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.video_response = None
            self.title = None
            self.video_url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        """Отображение информации об объекте класса для пользователей"""
        return f'{self.title}'


class PLVideo(Video):
    """класс для плейлиста  Ютуб канала. Наследуется от класса Video"""

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
