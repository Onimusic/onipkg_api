import os
import pandas as pd
import datetime


def read_bq():
    today = datetime.datetime.now().date()
    print(today)
    # Fazer a consulta no big query
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cred_bq.json"
    query = 'SELECT * FROM tutor-e-presave.tutor.insta_post_30'
    project = 'tutor-e-presave'
    df_post_period = pd.read_gbq(query=query, project_id=project)
    return df_post_period


def get_df_post_metrics_period():
    post_score_date = []
    post_like_date = []
    post_comment_date = []
    today = datetime.date.today()
    df_all_posts = read_bq()
    df_metric = df_all_posts.copy()
    days = [2, 3, 5, 7, 15, 30]
    for day in days:
        for idx, row in df_all_posts.iterrows():
            if abs(today - row['date_post']).days == day:
                post_score_date.append(df_all_posts.iloc[idx]['post_score'])
                post_like_date.append(df_all_posts.iloc[idx]['post_like'])
                post_comment_date.append(df_all_posts.iloc[idx]['post_comment'])
            else:
                post_score_date.append(None)
                post_like_date.append(None)
                post_comment_date.append(None)
        df_metric[f'post_score_{day}'] = post_score_date
        df_metric[f'post_like_{day}'] = post_like_date
        df_metric[f'post_comment_{day}'] = post_comment_date
        post_score_date = []
        post_like_date = []
        post_comment_date = []

    df_metric[['post_like_2', 'post_like_3', 'post_like_5', 'post_like_7', 'post_like_15', 'post_like_30',
              'post_comment_2', 'post_comment_3', 'post_comment_5', 'post_comment_7', 'post_comment_15',
              'post_comment_30']] = df_metric[
        ['post_like_2', 'post_like_3', 'post_like_5', 'post_like_7', 'post_like_15', 'post_like_30',
         'post_comment_2', 'post_comment_3', 'post_comment_5', 'post_comment_7', 'post_comment_15',
         'post_comment_30']].astype(pd.Int32Dtype())
    df_metric[['post_score_2', 'post_score_3', 'post_score_5', 'post_score_7', 'post_score_15'
        , 'post_score_30']] = df_metric[['post_score_2', 'post_score_3', 'post_score_5', 'post_score_7', 'post_score_15'
        , 'post_score_30']].astype(float)
    return df_metric
