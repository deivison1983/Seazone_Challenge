# imports
import pandas as pd
import math
import logging
import os

# functions

def loading_price(path):
    # loading
    df2 = pd.read_csv(path);
    
    return df2

def preparing_price(data):
    
    df2 = data.copy()
    # rename columns
    cols = ['ad_id', 'date', 'price', 'minimum_stay', 'available', 'av_for_checkin', 'aquisition_date', 
        'aquisition_date_max', 'check']
    df2.columns = cols
    
    # change type

    # date
    df2['date'] = pd.to_datetime(df2['date'])
    
    # av_for_checkin
    df2['av_for_checkin'] = df2['av_for_checkin'].apply( lambda x: True if x == 'true' else False)
    df2['av_for_checkin'] = df2['av_for_checkin'].astype(bool)
    
    # order
    df2 = df2.sort_values('ad_id', ascending = True)
    
    # feature engineering
    
    #price
    df2 = df2.loc[ df2['price'] < 19000 ].copy()
    df2['price'] = df2['price'].apply( lambda x: math.ceil(x) )
    df2['price'] = df2['price'].astype('int16')
    
    # dates
    df2['dia_add'] = df2['date'].dt.day
    df2['mes_add'] = df2['date'].dt.month
    df2['ano_add'] = df2['date'].dt.year
    
    df2['dia_semana'] = df2['date'].dt.weekday
    semana = {0: 'seg',1: 'ter',2: 'qua',3: 'qui',4: 'sex',5: 'sab',6: 'dom'}
    df2['dia_semana'] = df2['dia_semana'].map(semana)
    
    df2['dia_add']    = df2['dia_add'].astype('int8')
    df2['mes_add']    = df2['mes_add'].astype('int8')
    df2['ano_add']    = df2['ano_add'].astype('int16')
    df2['dia_semana'] = df2['dia_semana'].astype('category')
    
    # mes ocupacao
    df2['mes_ocupacao'] = df2['date'].dt.to_period('M')
    
    # faturamento
    df2['faturamento'] = df2.apply( lambda x: x['price'] if ( (x['av_for_checkin']==False) & (x['available']==False) ) else 0, axis = 1)
    
    # diarias
    df2['diarias'] = df2.apply( lambda x: 1 if ( (x['av_for_checkin']==False) & (x['available']==False) ) else 0, axis = 1)
    
    # dias por mes
    month_map = {1: 31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    df2['dias_mes'] = df2['mes_add'].map(month_map)
    
    # periodo anual dez-22 a nov-23
    df2['ano_add'] = '2022/2023'
    
    return df2


def data_consolidado(data):
    df2 = data.copy()
    
    # criando dataframe consolidado mes a mes
    consolidado_mes = ( df2[['ad_id', 'mes_ocupacao','faturamento','diarias', 'ano_add','dias_mes']]
                       .groupby(['ad_id', 'ano_add', 'mes_ocupacao', 'dias_mes'])
                       .agg(qty_diarias_mes = ('diarias', 'sum'),
                            faturamento_mes = ('faturamento', 'sum')).reset_index() )

    # dataframe imoveis consolidado ano
    consolidado_ano = ( df2[['ad_id', 'mes_ocupacao','faturamento','diarias', 'ano_add']]
                       .groupby(['ad_id', 'ano_add'])
                       .agg(qty_diarias_ano = ('diarias', 'sum'),
                            faturamento_ano = ('faturamento', 'sum') ).reset_index() )
    
    return consolidado_mes, consolidado_ano


def merge_data(data2, data4, df3):
    
    data3 = pd.merge(data2,data4, how='left', on= ['ad_id','ano_add']).reset_index()
    data3 = data3.drop('index',axis =1)
    
    # criando variaveis mensal
    data3['tax_oc_mes']     = data3.apply(lambda x: round( (x['qty_diarias_mes'] / x['dias_mes']), 2)   , axis = 1) 
    data3['tdm_oc_mes']     = data3.apply(lambda x: round( (x['faturamento_mes'] / x['qty_diarias_mes']), 2) if x['qty_diarias_mes'] != 0 else 0 , axis = 1) 
    data3['tdm_imovel_mes'] = data3.apply(lambda x: round( (x['faturamento_mes'] / x['dias_mes']), 2)   , axis = 1)
    
    # criando variaveis anual 
    data3['tax_oc_ano']     = data3.apply(lambda x: round( (x['qty_diarias_ano'] / 365), 2), axis = 1) 
    data3['tdm_oc_ano']     = data3.apply(lambda x: round( (x['faturamento_ano'] / x['qty_diarias_ano']), 2) if x['qty_diarias_mes'] != 0 else 0 , axis = 1) 
    data3['tdm_imovel_ano'] = data3.apply(lambda x: round( (x['faturamento_ano'] / 365), 2), axis = 1)
    
    # seleção de colunas
    data3 = data3[['ad_id', 'ano_add', 'mes_ocupacao', 'dias_mes', 'qty_diarias_mes','faturamento_mes',
                 'tax_oc_mes', 'tdm_oc_mes', 'tdm_imovel_mes','qty_diarias_ano','faturamento_ano',
                 'tax_oc_ano', 'tdm_oc_ano','tdm_imovel_ano']].copy()
    
    aux1 = df3[['ad_id','cidade','bairro','localized_star_rating_cat','listing_type']].copy()
    
    aux2 = pd.merge(data3,aux1, how='left', on= 'ad_id').reset_index()
    aux2 = aux2.drop('index',axis =1)

    aux2 = aux2.loc[(aux2['mes_ocupacao']>'2022-11')&(aux2['mes_ocupacao']<'2023-12')].copy()
    
    aux5 = {'Alto Perequê': 13,
        'Alto São Bento': 40,
        'Areal': 4,
        'Canto da Praia': 16,
        'Casa Branca': 48,
        'Cedro': 1,
        'Centro': 291,
        'Estaleirinho': 18,
        'Ilhota': 31,
        'Jardim Dourado': 59,
        'Jardim Praiamar': 10,
        'Meia Praia': 1350,
        'Morretes': 175,
        'Perequê': 151,
        'Rio Pequeno': 1,
        'Sertão do Trombudo': 3,
        'Sertãozinho': 9,
        'Tabuleiro dos Oliveiras': 42,
        'Vila Nova': 27,
        'Várzea': 19}

    aux2['qtd_imoveis_bairro'] = aux2['bairro'].map(aux5)
    
    aux3 = ( aux2[['ano_add','mes_ocupacao','cidade','bairro','tax_oc_mes','tdm_oc_mes','tdm_imovel_ano','faturamento_ano',
                   'ad_id','qty_diarias_mes','qty_diarias_ano','faturamento_mes','qtd_imoveis_bairro']]
            .groupby(['ano_add','cidade','bairro','qtd_imoveis_bairro'])
            .agg(qtd_diarias_anual = ('qty_diarias_mes','sum'),
                 qtd_anuncios_ano = ('ad_id','count'),
                 media_tax_mensal = ('tax_oc_mes','mean'),
                 media_tdm_oc_mes = ('tdm_oc_mes','mean'),
                 fat_anual = ('faturamento_mes','sum')).reset_index())
    
    
    aux3['fat/imovel']  = aux3.apply(lambda x: x['fat_anual']/x['qtd_imoveis_bairro'], axis = 1)
    aux3['fat/anuncio'] = aux3.apply(lambda x: x['fat_anual']/x['qtd_anuncios_ano'], axis = 1)
    aux3['fat/diaria']  = aux3.apply(lambda x: x['fat_anual']/x['qtd_diarias_anual'] if x['qtd_diarias_anual'] != 0 else 0, axis = 1)
    aux3

        
    return aux3


def dataframe_csv(df, path, name):
    # save dataframe
    aux1 = path + name
    df.to_csv(aux1, index = False)
    
    return None
        
