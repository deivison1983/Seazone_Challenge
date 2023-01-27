# imports
import pandas as pd
import logging
import os

from flow.metodos.host_v2           import loading_data, filtering_host
from flow.metodos.geo_bairros_v2    import loading_geo_data, search_bairros, save_csv
from flow.metodos.shapes_v2         import loading_geo_dataframe,shape_cities, shape_properties
from flow.metodos.details_v2        import data_cleaning
from flow.metodos.viva_real_v2      import preparing_data
from flow.metodos.price_v2          import loading_check, loading_features, merge_price, filtering_last_price, dataframe_csv
from flow.metodos.df_unificado_v2   import data_cleaning_unificado, merge_data_unificado, save_data
from flow.metodos.price_final_v2    import preparing_price, data_consolidado, merge_data, loading_price

def etl():
    print('etl ok')
    
    # logging
    path_log = '../etl_docs/3_arquivo_de_logs/'
    if not os.path.exists( path_log):
        os.makedirs(path_log)
        
    
    # price_v2 ------------------------------------------------
    
    logging.basicConfig(filename = path_log + 'price_log.txt',
                        format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        datefmt = '%Y-%m-%d %H:%M:%S',
                        level = logging.DEBUG)
    
    logger = logging.getLogger('price_log')
    
    # parameters
    
    path_price = '../data/data_base/Price_AV_Itapema.csv'
    path_merge = '../data/data_t1/'
    name_file  = 'Price_AV_Itapema_merge.csv'
    
    # job 1 loading data --> (ad_id - aquisition_date)
    data = loading_check(path_price)
    logger.info('loading data check done.')
    
    
    # job 2 loading data2 --> ( ad_id - price - minimum_stay - Available - aquisition_date - av_for_checkin )
    data2 = loading_features(path_price)
    logger.info('loading all data done.')
    
    # job 3 merge data e data2
    data3 = merge_price(data2,data)
    logger.info('merging dataframes done.')
    
    # job4 filtrar linhas ultimo webscraping
    data4 = filtering_last_price(data3)
    logger.info('filtering data done.')
    
    # job 5 salvar dataframe Price_AV_Itapema_merge.csv 
    dataframe_csv(data4, path_merge,name_file)
    logger.info('csv file saved.')
    
    
    
    # host_v2 -------------------------------------------------
    
#     logging.basicConfig( filename = path_log + 'host_log.txt',
#                          format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
#                          datefmt = '%Y-%m-%d %H:%M:%S',
#                          level = logging.DEBUG )
    logger = logging.getLogger('host_log')
    
    # parameters
    path_host   = '../data/data_base/Hosts_ids_Itapema.csv'
    path_folder = '../data/data_t1/'
    file_name   = 'host_ids_itapema_1.csv'
    
    # job1 loading data
    data = loading_data(path_host)
    logger.info('loading data done.')
    
    # job2 filtering and save csv
    filtering_host(data, path_folder, file_name)
    logger.info('csv file saved.')
    
    
    # geo_bairros_v2 ----------------------------------------------------------
    
#     logging.basicConfig( filename = path_log + 'data_bairros_log.txt',
#                          format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
#                          datefmt = '%Y-%m-%d %H:%M:%S',
#                          level = logging.DEBUG )
    logger = logging.getLogger('data_bairros_log')
    
    # parameters
    
    path_mesh   = '../data/data_base/Mesh_Ids_Data_Itapema.csv'
    path_folder = '../data/data_t1/' 
    name_file   = 'dataframe_bairros.csv'
    
    # job1 loading dataframe
    data = loading_geo_data(path_mesh)
    logger.info('loading data done.')
    
    # job2 adicionando bairros
    data = search_bairros(data)
    logger.info('all search was done.')
    
    #job salvando dataframe dataframe_bairros.csv
    save_csv(data, path_folder, name_file)
    logger.info('csv file saved.')
    
    
    # shapes_v2.py ------------------------------------------
    
#     logging.basicConfig(filename = path_log + 'shapes_log.txt',
#                         format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
#                         datefmt = '%Y-%m-%d %H:%M:%S',
#                         level = logging.DEBUG )
#     logger = logging.getLogger('shapes_log')
    
    # parameters
    path_shape_sc   = '../data/data_base/base_ibge/SC/SC_Municipios_2020.shp'
    path_properties = '../data/data_t1/dataframe_bairros.csv'

    
    # job1 loading geodataframe
    sc = loading_geo_dataframe(path_shape_sc)
    logger.info('loading geodata done.')
    
    # job2 loading dataframe_bairros
    data = loading_data(path_properties)
    logger.info('loading dataframe done.')
    
    # job3 criar shapes municipios
    shape_cities(sc)
    logger.info('shapes files cities created.')
    
    # job4 criar shape imóveis e salvar dataframe com pontos geometricos --> dataframe_bairros.csv
    shape_properties(data)
    logger.info('shapes files properties created.')
    
    
    # details_v2.py ------------------------------------------------
    
#     logging.basicConfig(filename = path_log + 'details_log.txt',
#                         format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
#                         datefmt = '%Y-%m-%d %H:%M:%S',
#                         level = logging.DEBUG )
    logger = logging.getLogger('details_log')
    
    # parameters
    path_hospede = '../data/data_base/Details_Data.csv'
    path_folder  = '../data/data_t1/'
    file_name    = 'details_1.csv'
    
    # job1 loading data
    data1 = loading_data(path_hospede)
    logger.info('loading data done.')
    
    # job2 data cleaning
    data2 = data_cleaning(data1)
    logger.info('data cleaning done.')
    
    # job3 save csv
    save_csv(data2,path_folder,file_name)
    logger.info('csv file saved.')
    
    
    # vivareal_v2.py
    
    logger = logging.getLogger('vivareal_log')
    
    # parameters
    path_viva   = '../data/data_base/VivaReal_Itapema.csv'
    path_folder = '../data/data_t1/'
    file_name   = 'vivareal_itapema_1.csv'
    
    # job1 loading data
    data = loading_data(path_viva)
    
    # job2 preparing data
    data2 = preparing_data(data)
    
    # job 3 save dataframe 
    save_csv(data2, path_folder, file_name)
    

    
    # df_unificado_v2.py
    
#     logging.basicConfig(filename = path_log + 'df_unificado_log.txt',
#                         format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
#                         datefmt = '%Y-%m-%d %H:%M:%S',
#                         level = logging.DEBUG )
    
    logger = logging.getLogger('df_unificado_log')
    
    # parameters
    
    path_bairros = '../data/data_t2/dataframe_bairros_2.csv'
    path_details = '../data/data_t1/details_1.csv'
    path_host    = '../data/data_t1/host_ids_itapema_1.csv'
    
    path_folder = '../data/data_t3/'
    file_name   = 'df_unificado.csv'
    
    # job1 loading dataframe_bairros
    data1 = loading_data(path_bairros)
    logger.info( 'Loding dataframe_bairros.csv')
    
    # job2 loading daframe details
    data2 = loading_data(path_details)
    logger.info( 'Loding dataframe details_1.csv')
    
     #job3 loading dataframe host_ids_itapema
    data3 = loading_data(path_host)
    logger.info( 'Loding dataframe host_ids_itapema.csv')
    
    # job4 cleaning data details
    data2 = data_cleaning_unificado(data2)
    logger.info( 'cleaning dataframe details_1.csv')
    
    # job5 merge dataframes
    data4 = merge_data_unificado(data2, data1,data3)
    logger.info( 'Dataframes merged')
    
    # job6 save dataframe df_unificado
    save_data(data4, path_folder, file_name)
    logger.info( 'Dataframe df_unificado.csv --> csv file saved')
    
    

    # price_final_v2 --------------------------------------------------
    
    logging.basicConfig(filename = path_log +'price_04_log.txt',
                        format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        datefmt = '%Y-%m-%d %H:%M:%S',
                        level = logging.DEBUG)
    logger = logging.getLogger('price_04_log')
    
    # parameters
    path_price    = '../data/data_t1/Price_AV_Itapema_merge.csv'
    path_df_uni   = '../data/data_t3/df_unificado.csv'
    path_price_04 = '../data/data_t4/'
    name_file  = 'price.csv'
    
    
    
    # job 1 loading dataframe Price_AV_Itapema_merge.csv
    df2 = loading_price(path_price)
    logger.info('loading data done.')
    
    # job 21 loading dataframe df_unificado
    df3 = loading_price(path_df_uni)
    logger.info('loading data done.')
    
    
    # job2 preparing data
    data = preparing_price(df2)
    logger.info('data preparing done.')
    
    # job3 dataframe imovel consolidados
    data2,data4 = data_consolidado(data)
    logger.info('dataframes created.')
    
    
    # job4 merge dataframes consolidados
    data5 = merge_data(data2, data4, df3)
    logger.info('merging dataframes done.')
        
    
    # job5 salvando dataframe price_04.csv
    dataframe_csv(data5,path_price_04,name_file)
    logger.info('csv file saved.')


    return None
