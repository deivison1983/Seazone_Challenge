# import
import pandas as pd
import logging
import os

# functions

def loading_data(path):
    df = pd.read_csv(path)
    return df

def data_cleaning_unificado(data):
    df = data.copy()
    df = df[['aquisition_date', 'ad_id', 'space', 'house_rules', 'amenities','safety_features',
             'number_of_bathrooms', 'number_of_bedrooms','number_of_beds', 'garagem', 'star_rating',
             'additional_house_rules', 'owner','number_of_guests', 'is_superhost',
             'number_of_reviews', 'cohosts','cleaning_fee', 'owner_id',
             'listing_type', 'localized_star_rating',
             'localized_star_rating_cat']].copy()

    df['house_rules'] = df['house_rules'].fillna('no_description')

    df['amenities']   = df['amenities'].fillna('no_description')
    
    return df

def merge_data_unificado(data1, data2, data3):
    
    aux1 = pd.merge(data1, data2, how='left', on= 'ad_id').reset_index()
    aux1 = aux1.drop('index',axis =1)
    
    aux2 = pd.merge(aux1,data3, how='left', on= 'owner_id').reset_index()
    aux2 = aux2.drop('index',axis =1)
    
    return aux2

def save_data(data,path,name):
    aux1 = path+name
    data.to_csv(aux1, index = False)
    
    return None

