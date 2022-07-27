import pandas as pd
import os
from youtube_data_api.df_thumbnails import get_youtube_data_api_csv, make_music_info
import traceback

def get_df_youtube_thumbnail():
    #Criar método para gerar o thumbnails.csv e o youtube_reports_os_device_tf_source bq
    df_video_music = pd.read_csv('videos_is_music.csv')
    df_youtube_musics = pd.read_csv('youtube_musics.csv')
    df_music_info = make_music_info(df_video_music, df_youtube_musics)
    df_thumb = get_youtube_data_api_csv(df_music_info)
    df_thumb = df_thumb.drop_duplicates()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "youtube_analytics/cred_bq.json"
    project = 'tutor-e-presave'
    # Teste tirar o limit para a versão final
    try:
        query = 'SELECT * FROM tutor-e-presave.tutor.youtube_reports_os_device_tf_source'
        df_tf_source = pd.read_gbq(query=query, project_id=project)
    except Exception as e:
        print(traceback.format_exc())

    df_agg_ratio = pd.DataFrame()

    #Mostrar todos os registros
    df_tf_source.dropna(inplace=True)

    df_tf_sum = pd.DataFrame()
    df_tf_sum[['video_id', 'views_all_tf']] = df_tf_source.groupby(['video_id'], as_index=False).sum()[['video_id',
                                                                                                        'views']]

    df_tf_related = pd.DataFrame()
    df_only_7 = df_tf_source[df_tf_source['traffic_source_type'] == 'Related video']
    df_tf_related[['video_id', 'views_tf_7']] = df_only_7.groupby(['video_id'], as_index=False).sum()[['video_id',
                                                                                                       'views']]

    df_ratio = df_tf_sum.merge(df_tf_related,on='video_id',how='inner')
    df_agg_ratio = pd.concat([df_agg_ratio, df_ratio], ignore_index=True)
    df_agg_ratio = df_agg_ratio.groupby('video_id', as_index=False).sum()

    df_agg_ratio['related_ratio'] = df_agg_ratio['views_tf_7'] / df_agg_ratio['views_all_tf']
    df_agg_ratio.drop(['views_tf_7', 'views_all_tf'], axis=1, inplace=True)

    df_youtube_ML = df_thumb.merge(df_agg_ratio, on='video_id', how='inner')
    return df_youtube_ML