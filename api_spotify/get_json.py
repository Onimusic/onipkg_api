from datetime import date
import base64
import datetime
import gzip
import pandas as pd
import requests
from io import BytesIO
import json
import re

class SpotifyAPI:
    """
    Classe que faz todas as funções relacionadas com a API do spotify, desde autenticação até a chamada do API Privada
    """
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = '6a66f11eae3f439ea6d759d9b68a4c68'
    client_secret = 'd0ee1bbb7a524c3e9f6724f5cb112b7e'
    token_url = "https://accounts.spotify.com/api/token"
    need_access = False

    def __init__(self, date, *args, **kwargs):
        """
        Função que recebe os parametros necessários para a autenticação
        Args:
            year: Ano da data de requisição
            month: Mês da data de requisição
            day: Dia da data de requisição
            *args:
            **kwargs:
        """
        super().__init__(*args, **kwargs)
        self.year = date.strftime('%Y')
        self.month = date.strftime('%m')
        self.day = date.strftime('%d')
        self.header = self.get_resource_header()
        self.licensor = 'onimusiccomerciodeartigosevangelicosltda'
        self.access_token_const = 'bWtDKUwu8yt-jRyINZbFjrjrwSRSZcYnEwzjOOj6VBophWqXRgUL11RiLKDRHjZPwhGJ72YQd4pbndB' \
                                  '0NDTsrSqsfDKbU4r3b1Hj3wN0hV5ZTbI5DuD34mYOaNz5_EtM8--aZrtQ2FvOD-MEu5mqz_kPkaAVonpw' \
                                  '7iMP3HKSDSty1TG7l5ZQWPP_4rh3DK-uV15cc8Ej40yw3XM5anD5RBX_62hioY'

    def get_client_credentials(self) -> str:
        """
        Recebe o client id e os client secrets e funciona para encodificar e decodificar as credenciais
        Returns: retorna as credenciais codificadas em base64
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret is None or client_id is None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self) -> dict:
        """
        utiliza as credenciais encodificadas com base 64 e nos retorna o header com as credenciais no formato que
        precisamos
        Returns: Header que possui a credencial encodificada em base 64
        """
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    @staticmethod
    def get_token_data() -> dict:
        """
        Returns: grant_type da credencial.
        """
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self) -> bool:
        """
        Realiza o processo de autenticação
        Returns: True em caso de sucesso
        """
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers, allow_redirects=True, verify=True)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self) -> str:
        """
        Utiliza o access token verificando a checagem se o mesmo está expirado
        Returns: Token de autenticação.
        """
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now or token is None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self) -> dict:
        """
        Utiliza a função get_access_token para pegar o token e o coloca em um formato de header para utilização
        Returns: Header no formato para utilização.
        """
        if not self.need_access:
            access_token = self.get_access_token()
            return {
                "Authorization": f"Bearer {access_token}"

            }
        return self.get_full_access_header()

    def get_data_streams(self, country) -> requests.models.Response:
        """
        Faz a request para o endpoint streams
        Returns: Respota da request
        """
        url = f'https://provider-api.spotify.com/v1/analytics/{self.licensor}/enhanced/streams/{self.year}/' \
              f'{self.month}/{self.day}/{country}'
        return requests.get(url, headers=self.header)

    def get_data_users(self) -> requests.models.Response:
        """
        Faz a request para o endpoint streams
        Returns: Respota da request
        """
        url = f'https://provider-api.spotify.com/v1/analytics/{self.licensor}/enhanced/users/{self.year}/{self.month}/'\
              f'{self.day}'
        return requests.get(url, headers=self.header)

    def get_data_tracks(self) -> requests.models.Response:
        """
        Faz a request para o endpoint tracks
        Returns: Respota da request
        """
        url = f'https://provider-api.spotify.com/v1/analytics/{self.licensor}/enhanced/tracks/{self.year}/' \
              f'{self.month}/{self.day}'
        return requests.get(url, headers=self.header)

    def get_data_aggregated_streams(self) -> requests.models.Response:
        """
        Faz a request para o endpoint aggregated streams
        Returns: Respota da request
        """
        url = f'https://provider-api.spotify.com/v1/analytics/{self.licensor}/enhanced/aggregatedstreams/{self.year}/' \
              f'{self.month}/{self.day}'
        return requests.get(url, headers=self.header)

    def get_full_access_header(self) -> dict:
        """
        Cria um header que possui o token com autorização, necessário para requests que necessitam de autorização
        Returns: Header com o token que possui autorização
        """
        return {
            "Authorization": f"Bearer {self.access_token_const}"
        }

    def get_tracks_bytesio(self) -> BytesIO:
        response_endpoint = self.get_data_tracks()
        decompressed_endpoint = gzip.decompress(response_endpoint.content)
        return BytesIO(decompressed_endpoint)

    def get_users_bytesio(self) -> BytesIO:
        response_endpoint = self.get_data_users()
        decompressed_endpoint = gzip.decompress(response_endpoint.content)
        return BytesIO(decompressed_endpoint)

    def get_streams_bytesio(self, country) -> BytesIO:
        response_endpoint = self.get_data_streams(country)
        decompressed_endpoint = gzip.decompress(response_endpoint.content)
        return BytesIO(decompressed_endpoint)

    def get_aggregated_streams_bytesio(self) -> BytesIO:
        response_endpoint = self.get_data_aggregated_streams()
        decompressed_endpoint = gzip.decompress(response_endpoint.content)
        return BytesIO(decompressed_endpoint)

    def get_users_tracks_aggregatedstreams_bytesio(self) -> (BytesIO, BytesIO, BytesIO):
        """
        Retorna 3 BytesIOs com os dados dos endpoints: tracks, users, aggregated streams
        """
        return self.get_users_bytesio(), self.get_tracks_bytesio(), self.get_aggregated_streams_bytesio()

    def organize_aggregated_streams(self) -> list:
        """
        Args:

        Returns:
            lista com as informações organizadas de acordo com o dataframe que deseja
        """
        organized_data = []
        aggregated_streams = self.get_aggregated_streams_bytesio()
        for line in aggregated_streams:
            parsed_data = json.loads(line)
            organized_data_line = {
                'song_name': parsed_data['trackv2']['name'],
                'isrc': parsed_data['trackv2']['isrc'],
                'href': parsed_data['trackv2']['href'],
                'streams': parsed_data['streams'],
                'skips': parsed_data['skips'],
                'saves': parsed_data['saves'],
            }
            organized_data.append(organized_data_line)
        aggregated_streams.close()
        organized_agg_streams = []
        for item in organized_data:
            for country in item['saves']['country']:
                local_saves_info = {
                    'track_name': item['song_name'],
                    'isrc': item['isrc'],
                    'uri': item['href'],
                    'country': country,
                    'streams': item['streams']['country'][country]['total'],
                    'saves': item['saves']['country'][country]['total'],
                    'free_saves': item['saves']['country'][country]['product'].get('free', 0),
                    'premium_saves': item['saves']['country'][country]['product'].get('premium', 0),
                    'skips': item['skips']['country'][country]['total'],
                }
                organized_agg_streams.append(local_saves_info)
        df_aggregated_streams = pd.DataFrame(organized_agg_streams)
        return df_aggregated_streams

    def get_json(self, iobyte_c: BytesIO) -> str:
        """
        Função que transforma iobyte em json para leitura posterior do pandas
        Args:
            iobyte_c: Arquivo do endpoint em iobyte
            name_io: Nome do arquivo que deseja em json
        """
        json_out = iobyte_c.read()
        json_out = json_out.decode("utf-8")
        return json_out

    def write_json(self, iobyte_c: BytesIO, name_io: str):
        json_out = self.get_json(iobyte_c)
        with open(f"{name_io}.json", "w") as f:
            # Writing data to a file
            f.write(json_out)

    def write_json_get_df_tracks(self):
        self.write_json(self.get_tracks_bytesio(), "tracks")
        df_tracks = self.json2df("tracks")
        return df_tracks


    def write_json_get_df_users(self):
        self.write_json(self.get_users_bytesio(), "users")
        df_users = self.json2df("users")
        return df_users

    @staticmethod
    def json2df(name_df: str) -> pd.DataFrame:
        """
        Faz a leitura do json muda a escrita e cria dataframe
        Args:
            name_df: Nome do arquivo em json que é feito a leitura

        Returns:
            df: Dataframe da leitura do json
        """
        with open(f'{name_df}.json', "r") as f:
            data = f.read()
            data = f'[{data}]'
            data = re.sub("}", "},", data)
            data = re.sub('},\n]', '}]', data)
            df = pd.json2df(data)
        return df

    def write_json_get_df_streams(self):
        """
        Função que pega cada ByteIO de stream agrega o endpoint de cada país e transforma em json
        Args:

        Returns:

        """
        # Usar for e cada vez pegar o objeto iobyte de streams e gerar json, agregar os json em um unico objeto
        df_users = self.json2df("users")
        countries = df_users['country'].unique()
        with open("streams.json", "w") as f:
            # Writing data to a file
            for country in countries:
                streams = self.get_streams_bytesio(country)
                json_out = self.get_json(streams)
                f.write(json_out)
        df_users = self.json2df("users")
        return df_users


def spotify_json(r_date):
    """
    Args:
    Função que gera os arquivos diários dos 4 endpoints sendo 3 json e 1 csv
        r_date: Data para solicitar a request na api do spotify
    Returns:
    """
    spotify = SpotifyAPI(r_date)
    spotify.write_tracks_json()
    spotify.write_users_json()
    spotify.write_stream_json()
    df_aggregated_streams = spotify.organize_aggregated_streams()
    df_aggregated_streams.to_csv(r'aggregated_streams.csv', index=None, header=True)