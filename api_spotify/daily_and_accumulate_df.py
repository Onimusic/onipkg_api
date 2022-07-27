import os
import time
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date
from get_json import spotify_json
from transform_df import SpotifyDFDay
import datetime


class SpotifyBQ:

    def __init__(self, starting_date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.starting_date = starting_date

    def daily_df(self):
        """

        Returns:
            Dataframe diário Spotify
        """
        running_date = self.starting_date
        print(f"python3 spotify_private_json.py {running_date.strftime('%d %m %Y')}")
        spotify_json(running_date)
        time.sleep(5)
        daily_df = SpotifyDFDay(self.starting_date, running_date)
        daily_df.json2pd()
        filepath_today = f"track_{self.starting_date.strftime('%d-%m-%Y')}_{running_date.strftime('%d-%m-%Y')}.csv"
        df_today = pd.read_csv(filepath_today)
        return df_today

    def accumulate_df(self):
        """

        Returns:
            Dataframe acumulativo
        """
        today = date.today()
        end_date = today + datetime.timedelta(days=-2)
        running_date = self.starting_date

        # Iniciando de starting_date enquanto for diferente de end_date agrega o dataframe antigo com o do dia
        while running_date != end_date:
            yesterday_date = running_date + relativedelta(days=-1)
            # gerando dataframe com a contagem diária
            print(f"python3 spotify_private_json.py {running_date.strftime('%d %m %Y')}")
            try:
                spotify_json(running_date)
                time.sleep(5)
                daily_df = SpotifyDFDay(self.starting_date, running_date)
                daily_df.json2pd()
                filepath_today = f"track_{self.starting_date.strftime('%d-%m-%Y')}_{running_date.strftime('%d-%m-%Y')}.csv"
                df_today = pd.read_csv(filepath_today)
            except Exception as e:
                print(e)
                continue

            filepath_yst = f"track_{self.starting_date.strftime('%d-%m-%Y')}_{yesterday_date.strftime('%d-%m-%Y')}.csv"
            if os.path.exists(filepath_yst):

                # lendo dataframe antigo
                df_yst = pd.read_csv(filepath_yst)

                #Remover o dataframe antigo(gerenciamento de memória)
                os.remove(filepath_yst)

                #Agrega o dataframe antigo com o novo
                df_out = pd.concat([df_today, df_yst], ignore_index=True)
                df_out.to_csv(filepath_today, index=None, header=True)
            running_date = running_date + datetime.timedelta(days=1)
        return df_out

class Tracks(SpotifyBQ):
    def __init__(self, starting_date):
        super().__init__(starting_date)
        self.df = self.daily_df()

    def set_columns_df(self):
        self.df.drop(['album__name', 'album__code', 'album__artist', 'track__artists'], axis=1, inplace=True)

    def get_df(self):
        return self.df


class Albums(SpotifyBQ):
    def __init__(self, starting_date):
        super().__init__(starting_date)
        self.df = self.daily_df()

    def set_columns_df(self):
        self.df.drop(['track__id', 'track__name', 'isrc', 'uri', 'track__artists'], axis=1, inplace=True)

    def get_df(self):
        return self.df


class Artists(SpotifyBQ):
    def __init__(self, starting_date):
        super().__init__(starting_date)
        self.df = self.daily_df()

    def set_columns_df(self):
        self.df.drop(['album__name', 'album__code', 'album__artist', 'track__id', 'track__name', 'isrc', 'uri'], axis=1,
                     inplace=True)

    def get_df(self):
        return self.df

