from src.channel import Channel
import json
import datetime
import isodate


class PlayList(Channel):
    def __init__(self, playlist_id):
        """Экземпляр инициализируется по id плейлиста. Дальше все данные будут подтягиваться по API."""
        self.playlist_id = playlist_id
        self.playlist_dict = self.get_service().playlists().list(id=playlist_id, part='snippet').execute()
        self.title = self.playlist_dict['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        # данные по видеороликам в плейлисте
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                                       part='contentDetails',
                                                                       maxResults=50,
                                                                       ).execute()
        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        # данные видеороликов
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                               id=','.join(video_ids)
                                                               ).execute()

    @property
    def total_duration(self):
        """возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста"""
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        max_likes_count = 0
        video_id = ''
        for video in self.video_response['items']:
            likes_count = int(video['statistics']['likeCount'])
            if max_likes_count < likes_count:
                max_likes_count = likes_count
                video_id = video['id']
        return f'https://youtu.be/{video_id}'
