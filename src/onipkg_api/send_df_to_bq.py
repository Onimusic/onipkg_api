import pandas as pd
import pandas_gbq
from google.oauth2 import service_account


def send_bq(service_acoount_file: str, df: pd.DataFrame, project_name: str, table_name: str, table_schema: list[dict],
            how: str = 'append'):
    """
    Função que envia os dados para o bigquery
    Args:
        service_acoount_file: Arquivo de credenciais do bigquery
        df: Dataframe que deseja ser enviado para o bigquery
        project_name: Nome do projeto do bigquery
        table_name: Nome da tabela junto com o nome do dicionário da table schema do cons.py
        table_schema: Schema da tabela
        how: Como deseja enviar os dados para o bigquery append, replace ou fail(se existir retorna raise)
    Returns:
    """
    credentials = service_account.Credentials.from_service_account_file(service_acoount_file)
    pandas_gbq.context.credentials = credentials
    pandas_gbq.context.project = project_name
    pandas_gbq.to_gbq(df, f"{table_name}", project_id=project_name, if_exists=how, table_schema=table_schema)
