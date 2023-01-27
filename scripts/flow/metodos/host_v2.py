# imports
import pandas as pd
import logging
import os



# functions
def loading_data(path):
    df_host = pd.read_csv(path)
    
    return df_host

def filtering_host(data, path, name):
    df_host = data.copy()
    df_host = df_host[['host_id', 'host_rating']].copy()
    aux0 = str(df_host.columns)
    #logger.debug('columns names: %s', aux0 )
    df_host.columns = ['owner_id', 'host_rating']
    
    # save csv
    aux1 = path+name
    df_host.to_csv(aux1, index = False)
    
    return None
