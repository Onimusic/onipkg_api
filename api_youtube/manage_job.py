from youtube_analytics.create_job import create_job
from youtube_analytics.delete_job import delete_job
from youtube_analytics.list_job import list_jobs
from youtube_analytics.list_reports import ReportsPeriod
import datetime
import pandas as pd

def manage_job(start_date, end_date):
    #Algoritmo main para selecionar a tarefa de job a ser feita
    #Seleção do modo de execução
    df_ids = pd.read_csv('youtube_data_api/music_ids.csv')
    print('Modos de ações dos jobs:')
    print('1 - Criar job')
    print('2 - Deletar job')
    print('3 - Listar jobs')
    print('4 - Listar reports de um job')
    mode = input('Digite o número da ação desejada: ')
    if mode == '1':
        print('Criando job')
        create_job()
    elif mode == '2':
        print('Deletando job')
        delete_job()
    elif mode == '3':
        print('Listando jobs')
        list_jobs()
    elif mode== '4':
        print('Listando reports de um job')
        report = ReportsPeriod(start_date, end_date)
        df_basic = report.get_basic_df(df_ids)
        df_os_device_tf_source = report.get_os_device_tf_source_df(df_ids)
        df_ad_revenue = report.get_ad_revenue_df(df_ids)
        df_all_revenue = report.get_all_revenue_df(df_ids)
        return df_basic, df_os_device_tf_source, df_ad_revenue, df_all_revenue
