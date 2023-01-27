# imports
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import logging
import os

# functions

def loading_geo_dataframe(path):
    sc = gpd.read_file(path)
    
    return sc

def loading_data(path):
    df = pd.read_csv(path)
    
    return df


def shape_cities(sc):
    # Municipios Itapema - Porto Belo - Balneario Camburiú
    porto = sc.loc[sc['NM_MUN'] == 'Porto Belo'].copy()
    balneario = sc.loc[sc['NM_MUN'] == 'Balneário Camboriú'].copy()
    itapema = sc[sc['NM_MUN'] == 'Itapema']
    camboriu = sc[sc['NM_MUN'] == 'Camboriú']
    
    # Salvando Shapefiles municipios pasta infogeo
    
    import os
    dir = '../data/data_t2/shapes/municipios/'
    # se a pasta nao existir python cria a pasta RJ-MUNIC
    if not os.path.exists(dir):
        os.makedirs(dir)
    # salvando 
    itapema.to_file(dir + 'itapema.shp')
    porto.to_file(dir + 'porto_belo.shp')
    balneario.to_file(dir + 'balneario.shp')
    camboriu.to_file(dir + 'camboriu.shp')
    
    return None

def shape_properties(data):
    df = data.copy()
    # criando pontos geometricos
    x = zip(df.longitude, df.latitude)
    geometry = [Point(x) for x in zip(df.longitude, df.latitude)]
    
    # criando geodataframe --> geo_dados
    crs = {'proj': 'latlong', 'ellps': 'WGS84', 'datum': 'WGS84', 'no_defs': True}
    geo_dados = gpd.GeoDataFrame(df, crs = crs, geometry = geometry)

    
    # salvando shapefile do geodados
    import os
    
    dir = '../data/data_t2/shapes/SC-DATASET'
    if not os.path.exists(dir):
        os.makedirs(dir)
    # salvando
    geo_dados.to_file(dir + '/DATASET.shp')
    
    # salvando csv do geodataframe geo_dados
    geo_dados.to_csv('../data/data_t2/dataframe_bairros_2.csv', index=False)
    
    return None
