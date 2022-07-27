import pandas as pd
import re
import pygeohash as gh
from config.cons import NAMECOLUMNS_SUM


class SpotifyDFDay:


    def __init__(self, start_date, run_date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.starting_date = start_date
        self.running_date = run_date

    def read_json(self, name_df: str) -> pd.DataFrame:
        """
        Faz a leitura do json muda a escrita e cria dataframe
        Args:
            name_df: Nome do arquivo em json que é feito a leitura

        Returns:
            df: Dataframe da leitura do json
        """
        f = open(f'{name_df}.json', "r")
        data = f.read()
        data = f'[{data}]'
        data = re.sub("}", "},", data)
        data = re.sub('},\n]', '}]', data)
        df = pd.read_json(data)
        return df

    def counting(self, old_col: str, new_col: str, value: str):
        """
        Faz a contagem de cada resultado da coluna selecionada
        Args:
            old_col: Nome da coluna original
            new_col: Nome da coluna que faz a contagem
            value: Valor da coluna original que vai ser contado

        Returns:

        """
        if old_col in self.my_columns:
            self.df_registros['spe_value'] = self.df_registros[old_col].mask(self.df_registros[old_col].ne(value))
            self.df_track[new_col] = self.df_registros.groupby(['track_id', 'track_name', 'isrc', 'uri'
                                                                    , 'album_name', 'album_code', 'album_artist'
                                                                    , 'track_artists']
                                                                   , as_index=False)['spe_value'].count()['spe_value']
        else:
            self.df_registros[new_col] = None

    def counting_all(self, old_col: str, new_col: str, value_list: list = None):
        """
        Faz a contagem para todos os valores da coluna selecionada
        Args:
            old_col: Nome da coluna original
            new_col:  Nome da coluna que faz a contagem
            value_list: Lista de valores da coluna original a serem contabilizados

        Returns:

        """
        if value_list is None:
            value_list = ['Y', 'N']

        for values in value_list:
            self.counting(old_col, f'{new_col}{values.lower()}', str(values))
    @staticmethod
    def locate(x):
        return gh.decode_exactly(x)

    def json2pd(self):
        """
        Limita as resposta do pandas para as opções selecionadas, faz a contagem definida pela função counting e salva
        o resultado em csv
        Returns:

        """
        # leitura do dataframe de streams
        df_streams = self.read_json('streams')
        df_users = self.read_json('users')
        df_tracks = self.read_json('tracks')
        df_aggregated_streams = pd.read_csv("aggregated_streams.csv")

        # deletando Colunas Desnecessárias
        df_streams.drop(['message', 'version', 'offline_timestamp', 'country', 'source_uri', 'utc_timestamp_offset'
                        , 'content_type_flag', 'completion_flag'], axis=1, inplace=True)
        df_users.drop(['message', 'version', 'access', 'product', 'partner', 'referral', 'region'], axis=1
                      , inplace=True)
        df_tracks.drop(['message', 'version'], axis=1, inplace=True)
        df_aggregated_streams.drop(['streams'], axis=1, inplace=True)



        #Geohash para latitude e longitude

        df_users['latitude']=df_users['geohash'].apply(lambda x:self.locate(x)[0] if x != '' else None)
        df_users['longitude']=df_users['geohash'].apply(lambda x:self.locate(x)[1] if x != '' else None)
        df_users.drop(['geohash'], axis=1, inplace=True)

        # join entre streams, track e user
        df_streams_new = df_streams.merge(df_tracks, on='track_id', how='inner')
        self.df_registros = df_streams_new.merge(df_users, on='user_id', how='inner')

        # Se source ou device_type tiver preenchido com outro valor substituir por others
        self.df_registros.loc[(self.df_registros['source'] != 'artist') & (self.df_registros['source'] != 'album')
                                    & (self.df_registros['source'] != 'collection')
                                    & (self.df_registros['source'] != 'others_playlist')
                                    & (self.df_registros['source'] != 'chart')
                                    & (self.df_registros['source'] != 'radio'), 'source'] = 'others'

        self.df_registros.loc[(self.df_registros['device_type'] != 'cell phone') &
                                    (self.df_registros['device_type'] != 'tablet') &
                                    (self.df_registros['device_type'] != 'personal computer') &
                                    (self.df_registros['device_type'] != 'smart tv device') &
                                    (self.df_registros['device_type'] != 'connected audio device') &
                                    (self.df_registros['device_type'] != 'built-in car application') &
                                    (self.df_registros['device_type'] != 'gaming console'), 'device_type'] = 'others'
        self.df_registros['date'] = self.running_date
        self.df_registros.to_csv('registros_3_endpoints.csv', index=None, header=True)
        df_aggregated_streams['date'] = self.running_date
        df_aggregated_streams.to_csv('aggregated_streams.csv', index=None, header=True)
        # adicionando as colunas string e contabilizando streams
        self.df_track = pd.DataFrame()
        self.df_track[['track_id', 'track_name', 'isrc', 'uri', 'album_name', 'album_code', 'album_artist',
                  'artists', 'streams']] = self.df_registros.groupby(['track_id', 'track_name', 'isrc', 'uri',
                                                                      'album_name', 'album_code','album_artist',
                                                                      'track_artists'], as_index=False)\
            .count()[['track_id', 'track_name', 'isrc', 'uri', 'album_name', 'album_code', 'album_artist'
                     , 'track_artists', 'user_id']]
        # lista com todos as colunas
        self.my_columns = list(self.df_registros)

        # agrupando por média
        self.df_track['stream_seconds_avg'] = self.df_registros.groupby(['track_id', 'track_name', 'isrc', 'uri'
                                                                    , 'album_name', 'album_code', 'album_artist'
                                                                    , 'track_artists'], as_index=False).mean()['length']
        self.counting_all('discovery_flag', 'discovery_flag_')
        self.counting_all('cached', 'streams_online_')
        self.counting_all('shuffle', 'shuffle_')
        self.counting_all('repeat_play', 'repeat_play_')
        self.counting_all('source', 'source__', ['artist','collection', 'others_playlist','album','radio','others'])
        self.counting_all('device_type', 'device__', ['personal computer', 'cell phone', 'tablet', 'smart tv device',
                                                     'connected audio device', 'gaming console',
                                                     'built-in car application', 'others'])
        self.counting_all('os', 'os_', ['Windows', 'Android', 'iOS', 'Mac', 'Linux', 'Browser', 'others'])
        self.counting_all('type', 'acccount_', ['paid', 'ad', 'trial', 'partner', 'partner-free', 'deleted'])
        self.counting_all('gender', '', ['male', 'female', ''])
        self.counting_all('age_group', 'age_', ['0-17', '18-22', '23-27', '28-34', '35-44', '45-59', '60-150'
                          , 'Unknown'])

        self.df_track = self.df_track.merge(df_aggregated_streams, on='uri', how='inner')
        self.df_track['date'] = self.running_date
        self.df_track.drop(['track_name_y', 'isrc_y', 'saves'], axis=1, inplace=True) #Deletar colunas desnecessárias
        # Transformar a coluna string to float
        self.df_track['stream_seconds_avg'] = self.df_track['stream_seconds_avg'].apply(pd.to_numeric, args=('coerce',))
        # Renomear as colunas
        print(list(self.df_track))
        self.df_track.columns = NAMECOLUMNS_SUM
        for columns in NAMECOLUMNS_SUM[10:56]:
            self.df_track[columns] = self.df_track[columns].astype(pd.Int32Dtype())
        # Transformar a coluna em string
        self.df_track['album__code'] = self.df_track['album__code'].astype(str)
        self.df_track.to_csv(
            f"track_{self.starting_date.strftime('%d-%m-%Y')}_{self.running_date.strftime('%d-%m-%Y')}.csv", index=None,
            header=True)
        return self.df_track