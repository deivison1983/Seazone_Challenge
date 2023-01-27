# imports
import pandas as pd
from datetime import datetime
import math
import logging
import os



# functions
def loading_check(path):
    dtype = {'airbnb_listing_id':'int64','aquisition_date':'category'}

    cols = ['airbnb_listing_id','aquisition_date']
    
    data_chunk = pd.read_csv( path, nrows = 43020080, dtype = dtype, low_memory=True, usecols = cols, chunksize=100000)
    
    chunk_data=[chunk for chunk in data_chunk]
    data = pd.concat(chunk_data)
    data['aquisition_date']   = data['aquisition_date'].astype('category')
    data['airbnb_listing_id'] = data['airbnb_listing_id'].astype('int64')
    
    chunk_data = []
    data_chunk = []
    
    # feature engineering
    
    # criando aquisition_date_max
    data['aquisition_date'] = data['aquisition_date'].apply(lambda x: x[0:10])
    aux1 = data[['airbnb_listing_id','aquisition_date']].groupby('airbnb_listing_id').max().reset_index()
    aux1 = aux1.set_index('airbnb_listing_id').T.to_dict('list')
    data['aquisition_date_max'] = data['airbnb_listing_id'].map(aux1)
    aux1=[]
    data['aquisition_date_max'] = data['aquisition_date_max'].apply(lambda x: ','.join(x) )
    
    # convertendo type
    data['aquisition_date_max'] = data['aquisition_date_max'].astype('category')
    data['aquisition_date'] = data['aquisition_date'].astype('category')
    data['airbnb_listing_id'] = data['airbnb_listing_id'].astype('category')
    
    # criando variavel check 
    data['check'] = data.apply(lambda x: True if x['aquisition_date']==x['aquisition_date_max'] else False, axis = 1)
    
    return data

def loading_features(path):

    # Loading
    dtype = {'airbnb_listing_id':'int64',
             'date':'category',
             'price':'float64',
             'minimum_stay':'int8',
             'aquisition_date':'category',
             'av_for_checkin':'category'}
    
    cols = ['airbnb_listing_id', 'date', 'price', 'minimum_stay', 'available', 'aquisition_date',
            'av_for_checkin']
    
    data_chunk = pd.read_csv( path, nrows = 43020080, dtype = dtype, low_memory=True, usecols = cols, chunksize=100000)
    
    chunk_data=[chunk for chunk in data_chunk]
    data2 = pd.concat(chunk_data)
    
    data2['date'] = data2['date'].astype('category')
    data2['aquisition_date'] = data2['aquisition_date'].astype('category')
    data2['airbnb_listing_id'] = data2['airbnb_listing_id'].astype('int64')
    
    chunk_data = []
    data_chunk = []
    
    return data2

def merge_price(data2,data):
    
    # # merging datasets
    
    data3 = pd.merge(data2, data, left_index=True, right_index=True)
    
    data3 = data3.drop(['airbnb_listing_id_y','aquisition_date_x'], axis = 1)
    
    data3.columns = ['airbnb_listing_id', 'date', 'price', 'minimum_stay', 'available', 'av_for_checkin',
                     'aquisition_date', 'aquisition_date_max', 'check']
    
    return data3

def filtering_last_price(data3):
    # selecionando as ultimas datas do webscraping
    data4 = data3.loc[data3['check']==True].copy()

    data4 = data4.loc[~(data4['av_for_checkin'].isna())].copy()
    
    return data4

def dataframe_csv(df, path, name):
    # save dataframe
    aux1 = path + name
    df.to_csv(aux1, index = False)
    
    return None

