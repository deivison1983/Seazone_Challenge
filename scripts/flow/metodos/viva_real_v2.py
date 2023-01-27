# imports
import pandas as pd
import re

# functions
def loading_data(path):
    df3 = pd.read_csv(path)
    
    return df3

def preparing_data(data):
    df3 = data.copy()
    
    # fill Na's
    
    # listing_title               11
    df3.listing_title = df3.listing_title.apply(lambda x: 'no_description' if pd.isna(x) else x )
    
    # listing_desc                95
    df3.listing_desc = df3.listing_desc.apply(lambda x: 'no_description' if pd.isna(x) else x )
    
    # unit_subtype             17312
    df3['unit_subtype'] = df3['unit_subtype'].apply(lambda x: 'no_description' if pd.isna(x) else x )
    
    # sale_price                1127
    df3 = df3.loc[~( (df3['sale_price'].isna())&(df3['rental_price'].isna()) )]
    df3['sale_price'] = df3['sale_price'].apply(lambda x: 1 if pd.isna(x) else x )
    
    # rental_price             16381
    df3['rental_price'] = df3['rental_price'].apply(lambda x: 0 if pd.isna(x) else x )
    
    # rental_period            16381
    df3['rental_period'] = df3['rental_period'].apply(lambda x: 'venda' if pd.isna(x) else x )
    df3['rental_period'].unique()
    
    # yearly_iptu               9938
    df3['yearly_iptu'] = df3['yearly_iptu'].apply(lambda x: 0 if pd.isna(x) else x )
    
    # monthly_condo_fee         9894
    df3['monthly_condo_fee'] = df3['monthly_condo_fee'].apply(lambda x: 0 if pd.isna(x) else x )
    
    # usable_area                  6
    df3['usable_area'] = df3['usable_area'].apply(lambda x: 0 if pd.isna(x) else x )
    
    # total_area                2072
    df3['total_area'] =  df3['total_area'].apply(lambda x: 0 if pd.isna(x) else x )
    
    # bathrooms                   40
    df3['bathrooms'] = df3['bathrooms'].apply(lambda x: 0 if pd.isna(x) else x )
    
    # bedrooms                    89
    df3['bedrooms'] =df3['bedrooms'].apply(lambda x: 0 if pd.isna(x) else x )
    
    # suites                    1239
    regex4 = r'(\d suite)'
    df3['suite2'] = df3['listing_desc'].apply(lambda x: (re.findall( regex4, x )))
    df3['suite2'] = df3['suite2'].apply(lambda x: ''.join(x) )
    df3['suite2'] = df3['suite2'].apply( lambda x: x[:1] )
    df3['suite2'] = df3['suite2'].apply(lambda x: '0' if x ==''else x).astype(int)
    df3['suites'] = df3.apply(lambda x: x['suite2'] if pd.isna(x['suites']) else x['suites'], axis = 1)
    
    # parking_spaces             785
    regex4 = r'(\d vaga)'
    df3['parking_spaces2'] = df3['listing_desc'].apply(lambda x: (re.findall( regex4, x )))
    df3['parking_spaces2'] = df3['parking_spaces2'].apply(lambda x: ''.join(x) )
    df3['parking_spaces2'] = df3['parking_spaces2'].apply( lambda x: x[:1] )
    df3['parking_spaces2'] = df3['parking_spaces2'].apply(lambda x: '0' if x ==''else x).astype(int)
    df3['parking_spaces']  = df3.apply(lambda x: x['suite2'] if pd.isna(x['suites']) else x['suites'], axis = 1)
    
    # address_neighborhood       942
    df3['address_neighborhood']  = df3['address_neighborhood'].fillna('no_description')
    
    # address_street            6735
    df3['address_street']  = df3['address_street'].fillna('no_description')
    
    # address_street_number     7199
    df3['address_street_number']  = df3['address_street_number'].fillna('no_description')
    
    # address_complement       17547
    df3['address_complement']  = df3['address_complement'].fillna('no_description')
    
    # advertiser_whatsapp       1373
    df3['advertiser_whatsapp']  = df3['advertiser_whatsapp'].fillna(0)
    
    # address_zipcode             17
    df3['address_zipcode']  = df3['address_zipcode'].fillna(0)
    
    df3 = df3.drop(['suite2','parking_spaces2'], axis = 1)
    
    
    # change type
    
    # datetime
    df3['aquisition_date'] = pd.to_datetime(df3['aquisition_date'])
    
    df3['bathrooms'] = df3['bathrooms'].astype(int)
    
    df3['bedrooms'] = df3['bedrooms'].astype(int)
    
    df3['suites'] = df3['suites'].astype(int)
    
    df3['parking_spaces'] = df3['parking_spaces'].astype(int)
    
    df3['address_zipcode'] = df3['address_zipcode'].astype(int)
    
    df3['advertiser_whatsapp'] = df3['advertiser_whatsapp'].astype(int)
    
    
    # filtering
    
    # removendo ids duplicados
    df3 = df3.drop_duplicates(subset = 'listing_id',ignore_index=True)
    
    # sale_price
    
    # remover valor max
    df3 = df3.loc[~(df3['sale_price']==134744000.00)].copy()
    
    # yearly_iptu
    df3['yearly_iptu'] = df3['yearly_iptu'].apply(lambda x: x/1000 if x>30000 else x)
    
    # usable_area
    df3['usable_area'] = df3.apply( lambda x: 142.96 if x['listing_id']==2580894364  else x['usable_area'], axis = 1)
    
    # total_area
    df3['total_area'] = df3.apply(lambda x: x['usable_area'] if (x['total_area'] == 1321273.00) else x['total_area'], axis = 1)
    df3['total_area'] = df3.apply(lambda x: x['usable_area'] if (x['total_area'] == 69700.00) else x['total_area'], axis = 1)
    
    df3 = df3.loc[~(df3['total_area']==589875.00)]
    
    # business_types
    df3['business_types'] = df3['business_types'].apply(lambda x: '["SALE", "RENTAL"]' if x == '["RENTAL", "SALE"]' else x)
    
    return df3

def save_csv(data, path, name):
    aux1 = path+name
    data.to_csv(aux1, index= False)
    
    return None
