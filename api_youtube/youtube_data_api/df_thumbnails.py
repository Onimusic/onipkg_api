from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
from config.cons import MUSIC_INFO_COLUMNS, API_YOUTUBE_DATA_KEY

class YoutubeApi:
    def __init__(self, credential_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credential_key = credential_key
        self.youtube = self.build_youtube()

    def build_youtube(self):
        """

        Returns: API Buildada

        """
        return build('youtube', 'v3', developerKey=self.credential_key)

    def get_video_contents(self, video_id):
        """
        Args:
            video_id: id de um video

        Returns: "snippets" de um video

        """
        try:
            return self.youtube.videos().list(part=['snippet', 'contentDetails'], id=video_id).execute()
        except:
            return ''

    @staticmethod
    def get_index_of_certain_id(id, dict_to_get_index):
        """

        Args:
            id: id de um item
            dict_to_get_index: dict que possui esse id

        Returns: index que ele se encontra

        """
        for i, item in enumerate(dict_to_get_index['items']):
            if item['id'] == id:
                return i

    def get_duration_from_video(self, video_id):
        return self.youtube.videos().list(id=video_id, part='contentDetails', maxResults=50).execute().get('items', {})[
            0].get('contentDetails', {}).get('duration', '')

    @staticmethod
    def duration2date(duration):
        if not 'H' in duration and 'M' in duration:
            duration = duration[2:-1].replace('M', ':')
            if ':' in duration:
                duration_date = datetime.strptime(duration, '%M:%S')
                duration_date = datetime.time(duration_date)
            else:
                duration_date = datetime.strptime(duration, '%M')
                duration_date = datetime.time(duration_date)
        else:
            duration_date = None
        return duration_date
        
def make_music_info(df_video_music, df_youtube_musics):
    df_video_music = df_video_music[['custom_id', 'isrc']]
    df_youtube_musics = df_youtube_musics[['track', 'title', 'isrc', 'name']]
    df_music_info = df_video_music.merge(df_youtube_musics, on='isrc', how='inner')
    df_music_info = df_music_info[['name', 'track', 'custom_id', 'isrc']]
    df_music_info.columns = MUSIC_INFO_COLUMNS
    return df_music_info

def get_youtube_data_api_csv(df_music_info):
    df_data_api = pd.DataFrame()
    youtube = YoutubeApi(API_YOUTUBE_DATA_KEY)
    ids = list(df_music_info['video_id'])
    for idx in range(len(ids) // 50):
        ids_50 = ids[50 * idx:50 * (idx + 1)]
        json_50 = youtube.get_video_contents(ids_50)
        for items in json_50.get('items'):
            video_id = items.get('id')
            snippet = items.get('snippet')
            title = snippet.get('title')
            published_at = snippet.get('publishedAt')
            thumbnail = snippet.get('thumbnails').get('high').get('url')
            duration = items.get('contentDetails').get('duration')
            duration_date = youtube.duration2date(duration)
            channel_name = snippet.get('channelTitle')
            my_dict = {'video_id': video_id, 'published_at': published_at, 'thumbnail': thumbnail,
                       'duration': duration_date}
            df_data_api = pd.concat([df_data_api, pd.DataFrame(my_dict, index=[0])], ignore_index=True)
    df_data_api = df_data_api[df_data_api['duration'].notna()]
    df_data_api = df_data_api.merge(df_music_info, on='video_id', how='inner')
    df_data_api.drop(['isrc'], axis=1, inplace=True)
    df_data_api = df_data_api[['artist', 'track', 'video_id', 'thumbnail', 'duration', 'published_at']]
    df_data_api.to_csv('thumbnails.csv', index=None, header=True)

    return df_data_api
