import pandas as pd
from api_ct import CtGetDF


def all_post(starting_date):
    df_accounts = pd.read_csv('accounts.csv')
    pags = 0
    crowdtangle = CtGetDF()
    df = crowdtangle.get_df_post(list_ids=1497075, start_date=starting_date, count=100, sort_by='date',
                                            offset=pags)
    df_new = pd.DataFrame.copy(df)
    while not df_new.empty:
        try:
            pags += 1
            df_new = crowdtangle.get_df_post(list_ids=1497075, start_date=starting_date, count=100, sort_by='date',
                                             offset=pags * 100)
            df = pd.concat([df, df_new], ignore_index=True)
        except Exception as e:
            print(e)
            continue
    df_posts = df_accounts.merge(df,left_on='name',right_on='account_name',how='left')
    df_posts[['post_like', 'post_comment', 'photo_width', 'photo_height', 'account_subscriber']] = \
    df_posts[['post_like', 'post_comment', 'photo_width', 'photo_height', 'account_subscriber']].astype(pd.Int32Dtype())


    df_posts['account_id'] = df_posts['account_id'].astype(str)
    df_posts['account_id'] = df_posts['account_id'].str.replace('.0', '')
    df_posts.drop(['name', 'handle'], axis=1, inplace=True)

    return df_posts