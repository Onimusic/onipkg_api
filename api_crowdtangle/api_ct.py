import requests
import datetime
import pandas as pd
from config.cons import HEADER

class CtGetDF:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.today = datetime.datetime.now().date()

    @staticmethod
    def create_payload_leader(account_ids=None, count=None, end_date=None, list_id=None, offset=None,
                              order_by=None, sort_by=None, start_date=None):
        """
        Cria o payload que será utilizado na request
        Args:
            account_ids: ids das contas que queremos utilizar
            count: quantidade de itens que queremos retornar
            end_date: dia que deve parar a busca
            list_id: The list of the leaderboard to retrieve.
            offset: The number of rows to offset.
            order_by: the order of the sort. asc ou desc(ascendente ou descendente)
            sort_by: The method by which the accountStatistics are sorted.	total_interactions or interaction_rate
            start_date: The startDate of the leaderboard rage.

        Returns: Payload com as informações colocadas

        """
        payload = {}
        if account_ids is not None:
            payload.update({'accountIds': account_ids})
        if count is not None:
            payload.update({'count': count})
        if end_date is not None:
            payload.update({'endDate': end_date})
        if list_id is not None:
            payload.update({'listId': list_id})
        if offset is not None:
            payload.update({'offset': offset})
        if order_by is not None:
            payload.update({'orderBy': order_by})
        if sort_by is not None:
            payload.update({'sortBy': sort_by})
        if start_date is not None:
            payload.update({'startDate': start_date})
        return payload

    def create_payload_post(self, accounts=None, branded_content=None, count=None, end_date=None, include_history=None,
                       language=None, list_ids=None, min_interactions=None, offset=None, page_admin_top_country=None,
                       search_term=None, sort_by=None, start_date=None, timeframe=None, types=None, verified=None):

        payload = {'accounts': accounts, 'brandedContent': branded_content, 'count': count, 'endDate': end_date,
                   'includeHistory': include_history, 'language': language, 'listIds': list_ids,
                   'minInteractions': min_interactions, 'offset': offset, 'pageAdminTopCountry': page_admin_top_country,
                   'searchTerm': search_term, 'sortBy': sort_by, 'startDate': start_date, 'timeframe': timeframe,
                   'types': types, 'verified': verified}

        payload = {k: v for k, v in payload.items() if v}
        return payload

    @staticmethod
    def make_request_leader(payload=None):
        """
        Retorna o link de request para API
        Args:
            payload: payload que será utilizado na request

        Returns: objeto tipo request

        """
        return requests.get(
            'https://api.crowdtangle.com/leaderboard', headers=HEADER, params=payload
        )

    @staticmethod
    def make_request_post(payload=None):
        return requests.get(
            'https://api.crowdtangle.com/posts', headers=HEADER, params=payload
        )


    def organize_info_leader(self, account_ids=None, count=None, end_date=None, list_id=None, offset=None,
                             order_by=None, sort_by=None, start_date=None):
        """

        Args:
            account_ids: ids das contas que queremos utilizar
            count: quantidade de itens que queremos retornar
            end_date: dia que deve parar a busca
            list_id: The list of the leaderboard to retrieve.
            offset: The number of rows to offset.
            order_by: the order of the sort.
            sort_by: The method by which the accountStatistics are sorted.
            start_date: The startDate of the leaderboard rage.

        Returns: informação organizada
"""
        payload = self.create_payload_leader(account_ids, count, end_date, list_id, offset,
                                      order_by, sort_by, start_date)
        response = self.make_request_leader(payload)
        general_info = []
        for item in response.json()['result']['accountStatistics']:
            info_from_artists = {
                'id': item.get('account', '{}').get('id'),
                'name': item.get('account', '{}').get('name'),
                'handle': item.get('account', '{}').get('handle'),
                'subscriber': item.get('account', '{}').get('subscriberCount'),
                'interaction': item['summary'].get('totalInteractionCount'),
                'post': item['summary'].get('postCount'),
                'interaction_rate': item['summary'].get('interactionRate'),
                'favorite': item['summary'].get('favoriteCount'),
                'comment': item['summary'].get('commentCount'),

                'album_interaction': item.get('breakdown', {}).get('album', {}).get('totalInteractionCount'),
                'album_post': item.get('breakdown', {}).get('album', {}).get('postCount'),
                'album_interaction_rate': item.get('breakdown', {}).get('album', {}).get('interactionRate'),
                'album_favorite': item.get('breakdown', {}).get('album', {}).get('favoriteCount'),
                'album_comment': item.get('breakdown', {}).get('album', {}).get('commentCount'),

                'photo_interaction': item.get('breakdown', {}).get('photo', {}).get('totalInteractionCount'),
                'photo_post': item.get('breakdown', {}).get('photo', {}).get('postCount'),
                'photo_interaction_rate': item.get('breakdown', {}).get('photo', {}).get('interactionRate'),
                'photo_favorite': item.get('breakdown', {}).get('photo', {}).get('favoriteCount'),
                'photo_comment': item.get('breakdown', {}).get('photo', {}).get('commentCount'),

                'video_interaction': item.get('breakdown', {}).get('video', {}).get('totalInteractionCount'),
                'video_post': item.get('breakdown', {}).get('video', {}).get('postCount'),
                'video_interaction_rate': item.get('breakdown', {}).get('video', {}).get('interactionRate'),
                'video_favorite': item.get('breakdown', {}).get('video', {}).get('favoriteCount'),
                'video_comment': item.get('breakdown', {}).get('video', {}).get('commentCount'),
                'date': start_date,
            }
            general_info.append(info_from_artists)
        return general_info

    def organize_info_post(self, accounts=None, branded_content=None, count=None, end_date=None,
                                       include_history=None, language=None, list_ids=None, min_interactions=None,
                                       offset=None, page_admin_top_country=None, search_term=None, sort_by=None,
                                       start_date=None, timeframe=None, types=None, verified=None):

        # Define os valores das variáveis
        payload = self.create_payload_post(accounts, branded_content, count, end_date, include_history, language,
                                           list_ids, min_interactions, offset, page_admin_top_country, search_term,
                                           sort_by, start_date, timeframe, types, verified)

        # Faz o request com os valores definidos
        response = self.make_request_post(payload)
        general_info = []

        # Organizar os dados
        for item in response.json()['result']['posts']:

            date_r = item.get('date')
            if date_r:
                date_list = item.get('date').split('-')
                date_r = datetime.datetime(int(date_list[0]), int(date_list[1]), int(date_list[2][:2])).date()
            description = item.get('description')
            if description:
                description = description.replace('\n', ' ')
            video_url = item.get('media')[0].get('type') == 'video'
            if video_url:
                video_url = item.get('media')[0].get('url')
                photo_url = item.get('media')[1].get('url')
                photo_height = item.get('media')[1].get('height')
                photo_width = item.get('media')[1].get('width')

            else:
                video_url = None
                photo_url = item.get('media')[0].get('url')
                photo_height = item.get('media')[0].get('height')
                photo_width = item.get('media')[0].get('width')

            info_from_post = {

                # dict.get('key','value') if key exist return the value of dict if not 'value'
                'account_id': item.get('account').get('id'),
                'account_name': item.get('account').get('name'),
                'account_handle': item.get('account').get('handle'),
                'account_subscriber': item.get('account').get('subscriberCount'),
                'account_profile_picture': item.get('account').get('profileImage'),
                'account_url': item.get('account').get('url'),
                'account_verified': item.get('account').get('verified'),
                'account_language': item.get('languageCode'),
                'post_type': item.get('type'),
                'post_description': description,
                'post_url': item.get('postUrl'),
                'video_url': video_url,
                'photo_url': photo_url,
                'photo_width': photo_width,
                'photo_height': photo_height,
                'post_score': item.get('score', 0),
                'post_like': item.get('statistics').get('actual').get('favoriteCount'),
                'post_comment': item.get('statistics', '').get('actual', '').get('commentCount'),
                'date_post': date_r
            }
            general_info.append(info_from_post)
        return general_info

    def get_df_leader(self, account_ids=None, count=None, end_date=None, list_id=None, offset=None,
                               order_by=None, sort_by=None, start_date=None) -> pd.DataFrame:
        """

        Args:
            account_ids: ids das contas que queremos utilizar
            count: quantidade de itens que queremos retornar
            end_date: dia que deve parar a busca
            list_id: The list of the leaderboard to retrieve.
            offset: The number of rows to offset.
            order_by: the order of the sort.
            sort_by: The method by which the accountStatistics are sorted.
            start_date: The startDate of the leaderboard rage.
            name: Nome do csv

        Returns: csv com as informações

        """
        info = self.organize_info_leader(account_ids, count, end_date, list_id, offset,
                                                   order_by, sort_by, start_date)
        df = pd.DataFrame(info)
        df[['interaction', 'post', 'favorite', 'comment', 'album_interaction', 'album_post', 'album_favorite',
            'album_comment', 'photo_interaction', 'photo_post', 'photo_favorite', 'photo_comment', 'video_interaction',
            'video_post', 'video_favorite', 'video_comment']] = \
            df[['interaction', 'post', 'favorite', 'comment', 'album_interaction', 'album_post', 'album_favorite',
                'album_comment', 'photo_interaction', 'photo_post', 'photo_favorite', 'photo_comment',
                'video_interaction','video_post', 'video_favorite', 'video_comment']].astype(pd.Int32Dtype())
        return df
    
    def get_df_leader_accumulate(self, start_date_accumulate, account_ids=None, count=None, list_id=None, offset=None,
                      order_by=None, sort_by=None) -> pd.DataFrame:

        '''
        Args:
            start_date_accumulate: date to start the aggretated on dataframe
            account_ids: id to account
            count: number of item to search
            list_id: id to a group of account
            offset: search from offset+1 to offset+count
            order_by: the order of the sort.
            sort_by: The method by which the accountStatistics are sorted.

        Returns:
            Dataframe accumulate from, start_date_acumulate to today
        '''

        running_date = start_date_accumulate
        df = pd.DataFrame()
        while running_date != self.today:
            try:
                df_new = self.get_df_leader(list_id=list_id, start_date=running_date.strftime('%Y-%m-%d'),
                                              end_date=(running_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                                              count=100)
                df = pd.concat([df, df_new], ignore_index=True)
                running_date = running_date + datetime.timedelta(days=1)
                print(running_date)
            except Exception:
                continue
        return df

    def get_df_post(self, accounts=None, branded_content=None, count=None, end_date=None,
                               include_history=None, language=None, list_ids=None, min_interactions=None, offset=None,
                               page_admin_top_country=None, search_term=None, sort_by=None, start_date=None,
                               timeframe=None, types=None, verified=None):

        info = self.organize_info_post(accounts, branded_content, count, end_date, include_history, language, list_ids,
                                       min_interactions, offset, page_admin_top_country, search_term, sort_by,
                                       start_date, timeframe, types, verified)
        df = pd.DataFrame(info)
        return df
