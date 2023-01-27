# imports
import pandas as pd
from geopy.geocoders import Nominatim
import logging
import os

# functions
# loading 

def loading_geo_data(path):
    #loading
    df2 = pd.read_csv(path)
    # selection variables to seach bairros
    df2 = df2[['airbnb_listing_id', 'latitude', 'longitude']].copy()
    df2 = df2.drop_duplicates(subset=['airbnb_listing_id'],ignore_index=True)
    
    return df2

def search_bairros(data):
    
    df2 = data.copy()
    #rename columns
    df2.columns = ['ad_id', 'latitude', 'longitude']
    
    # adicionando bairros
    df2['bairro'] = 'no_description'
    df2['cidade'] = 'no_description'
    # localizando bairros
    geolocator = Nominatim( user_agent = 'infogeo')
    
    for i in range( len(df2)):
        query = str( df2.loc[i,'latitude'] ) + ',' + str( df2.loc[i,'longitude'] )
        
        response = geolocator.reverse( query)
            
        if  'suburb' in response.raw['address']:
            df2.loc[i, 'bairro' ] = response.raw['address']['suburb']
        if  'town' in response.raw['address']:
            df2.loc[i, 'cidade' ] = response.raw['address']['town']
        #logger.debug('bairro localizado %s',df2.loc[i, 'bairro' ])
    
    # Alterando bairros nao localizados nominatim
    df2['bairro'] = df2.apply(lambda x: 'Areal' if ( (x['cidade']=='Itapema')&(x['bairro']=='no_description') ) else x['bairro'], axis = 1)
    
    df2['bairro'] = df2.apply(lambda x: 'Estaleirinho' if ( (x['cidade']=='no_description')&(x['bairro']=='no_description') ) else x['bairro'], axis = 1)
    
    df2['cidade'] = df2.apply(lambda x: 'Balneário Camboriú' if ( (x['cidade']=='no_description')&(x['bairro']=='Estaleirinho') ) else x['cidade'], axis = 1)
    
    return df2

def save_csv(data,path,name_file):
    aux1 = path+name_file
    data.to_csv(aux1, index = False)
    
    return None
