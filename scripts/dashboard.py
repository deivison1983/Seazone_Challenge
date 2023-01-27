import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np

from streamlit_folium import folium_static

import folium
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap

import plotly.express as px
from datetime import datetime

from PIL import Image

st.set_page_config(layout='wide')

@st.cache(allow_output_mutation = True)
def get_data(path):
    data = pd.read_csv(path)
    return data
    
@st.cache(allow_output_mutation = True)
def get_data2(path2):
    data2 = pd.read_csv(path2)
    return data2
    
@st.cache(allow_output_mutation = True)
def get_data3(path3):
    data3 = pd.read_csv(path3)
    return data3

@st.cache(allow_output_mutation = True)
def get_data4(path4):
    data4 = gpd.read_file(path4)
    return data4

@st.cache(allow_output_mutation = True)
def get_data5(path5):
    data5 = gpd.read_file(path5)
    return data5

@st.cache(allow_output_mutation = True)
def get_data6(path6):
    data6 = gpd.read_file(path6)
    return data6

@st.cache(allow_output_mutation = True)
def get_data7(path7):
    data7 = gpd.read_file(path7)
    return data7

@st.cache(allow_output_mutation = True)
def get_data8(path8):
    data8 = gpd.read_file(path8)
    return data8


# # funcoes
# def set_feature(data):

#     return data

def overview_data(data):
    
    imagem = Image.open('./data/data_base/seazone.png')
    st.sidebar.image(imagem)
    st.title('Seazone Challenge - Data Scientist')
    st.header('Data Overview')
    st.markdown('### Detalhes imóveis - Amostra dataset')
    
    # filtro detalhes imoveis
    st.sidebar.header('Data Overview')
    f_attributes = st.sidebar.multiselect('Selecione as colunas', data.columns)
    if f_attributes != []:
        fa = data.loc[:, f_attributes]
    else:
        fa = data.copy()
        
    # dataset imoveis
    st.write(fa.head(50))
    st.write('Número total de imóveis: {} -->'.format(fa.shape[0]),'Número total de variáveis: {}'.format(fa.shape[1]) )
    
    
    # filtro cidade
    f_cidade = st.sidebar.multiselect('Escolha a cidade',sorted(set(data['cidade'].unique())))
    if f_cidade != []:
        data = data.loc[data['cidade'].isin(f_cidade)]
    else:
        data = data.copy()
    # filtro bairro
    f_zipcode = st.sidebar.multiselect('Escolha o bairro',sorted(set(data['bairro'].unique())))
    if f_zipcode != []:
        data = data.loc[data['bairro'].isin(f_zipcode)]
    else:
        data = data.copy()
    
    # colunas 
    c1, c2 = st.columns((1, 1))
    
    # gerando agrupamentos
    df1 = data[['ad_id','cidade', 'bairro']].groupby(['cidade','bairro']).count().reset_index()
    df2 = data[['number_of_bedrooms', 'bairro']].groupby('bairro').sum().reset_index()
    df3 = data[['number_of_guests', 'bairro']].groupby('bairro').sum().reset_index()
    
    # uniao dataframes
    m1 = pd.merge(df1, df2, on='bairro', how='inner')
    m2 = pd.merge(m1, df3, on='bairro', how='inner')
    df = m2
    
    # plotando dataset 
    c1.markdown('### Resumo Cidade e Bairro')
    df.columns = ['Cidade','Bairro','TOTAL_imóveis', 'Total_de_Quartos', 'Capacidade_de_hóspedes']
    c1.dataframe(df, height=600)
    c1.write('Total de imóveis disponíveis = {}'.format(data.shape[0]) )

    # calculando metricas
    num_attributes = data[['number_of_bathrooms', 'number_of_bedrooms','number_of_beds','star_rating','cleaning_fee']]
    media   = pd.DataFrame(num_attributes.apply( np.mean)  )
    mediana = pd.DataFrame(num_attributes.apply( np.median))
    std     = pd.DataFrame(num_attributes.apply( np.std)   )
    max_    = pd.DataFrame(num_attributes.apply( np.max)   ) 
    min_    = pd.DataFrame(num_attributes.apply( np.min)   )
    
    # unindo metricas
    df = pd.concat([ min_, max_, media, mediana, std], axis=1).reset_index()
    df.columns = ['ATTRIBUTES', 'MIN', 'MAX', 'MEAN', 'MEDIAN', 'STD']
    
    
    #plotando dataset
    c2.markdown('### Visão geral dos imóveis')
    c2.dataframe(df.style.format({'MIN': '{:.2f}','MAX': '{:.2f}','MEAN': '{:.2f}','MEDIAN': '{:.2f}','STD': '{:.2f}'}), height = 300)

    return None



def portfolio_density(data2, data, data4,data5,data6,data7,data8):
    '''Função que exibe a distribuicao geografica dos imoveis nos municipios com layout interativo
    
    parametros:
    -----------
    data2: dataframe_bairros_2 informacoes geograficas imoveis
    data: dataframe df_unificado informacoes imoveis
    data4: geodataframe municipio itapema
    data5: geodatframe municipio porto belo
    data6: geodataframe municipio balneario camburiu
    data7: geodataframe imoveis
    data8: geodataframe municipio camburiu
    
    '''

    st.title('Region Overview')
    
    df = data6
    
    # filtro limite da cidade mapa
    st.sidebar.header('Region Overview')
    f_cidade_mapa = st.sidebar.selectbox('Escolha a cidade do mapa',sorted(set(data['cidade'].unique())),index = 2)
    if f_cidade_mapa != []:
        if f_cidade_mapa == 'Itapema':
            df = data4
            aux0 = data7.loc[data7['cidade']=='Itapema'].copy()
        if f_cidade_mapa == 'Porto Belo':
            df = data5
            aux0 = data7.loc[data7['cidade']=='Porto Belo'].copy()
        if f_cidade_mapa == 'Balneário Camboriú':
            df = data6 
            aux0 = data7.loc[data7['cidade']=='Balneário Camboriú'].copy()
        if f_cidade_mapa == 'Camboriú':
            df = data8
            aux0 = data7.loc[data7['cidade']=='Camboriú'].copy()
    else:
        df = data4

        
    # filtro bairro mapa
    f_bairro = st.sidebar.multiselect('Escolha os bairros do mapa',sorted(set(aux0['bairro'].unique())))
    if f_bairro != []:
        aux0 = aux0.loc[aux0['bairro'].isin(f_bairro)]
    else:
        aux0 = aux0.copy()
        
    
    # colunas densidade de imóveis e 
    c1, c2 = st.columns((1, 1))
    
    c1.markdown('### Portfolio Density')

    # Base Map - Folium
    #st.dataframe(df[['NM_MUN','AREA_KM2']])
    st.write(f"Área do município {str(df['NM_MUN'][0])}: {df['AREA_KM2'][0]} KM2")
    
    #centroid do mapa
    y = data4.centroid.y.iloc[0]
    x = data4.centroid.x.iloc[0]
    density_map = folium.Map([y,x], default_zoom_start=5)
    
    # Limite da cidade selecionada
    density_map.choropleth(df,
                           name= "Limites da cidade",
                           line_color="Black",
                           line_weight=3,
                           fill_opacity=0)
    

    # cluster do imoveis
    cluster = MarkerCluster()
    # inserindo marcadores da cidade e bairros selecionados
    for item in aux0.itertuples():
        # adicionar ao cluster os filhos
        cluster.add_child(folium.Marker( location=[item.latitude, item.longitude],
                                        popup="<h4>"+str(item.bairro)+"</h4> <h5>"+str(item.cidade)+"</h5> <p>ad_id: "+str(item.ad_id)+"</p>",
                                        icon=folium.Icon(color='red',
                                                         prefix='fa', 
                                                         icon='fas fa-home')
                                       )
                         )
    # adiciona o filho a base    
    density_map.add_child(cluster)
    
    # layer
    folium.LayerControl('topleft', collapsed= True).add_to(density_map)
    # plota   
    with c1:
        folium_static(density_map)

        
    # Region price map
    c2.markdown('### Média da Tarifa diária mensal')
    
    # heatmap precisa de uma lista com latitude longitude e um peso
    # criando o peso
    
    # tarifa diaria media ocupacao mensal
    aux1 = data3[['bairro','media_tdm_oc_mes']].copy()
    peso = aux1['media_tdm_oc_mes'].max()
    aux1['peso'] = aux1['media_tdm_oc_mes'].apply( lambda x: x / peso )
    aux1 = aux1.drop('media_tdm_oc_mes', axis = 1)
    aux1 = aux1.set_index('bairro')
    aux1 = aux1.to_dict()
    aux1 = aux1['peso']
    aux2 = data.copy()
    aux2['tarifa'] = aux2['bairro'].map(aux1)
    
    # criando coordenada + peso para o heatmap
    aux3 = []
    for i in range(len(aux2)):
        aux3.append([aux2['latitude'][i],
                     aux2['longitude'][i],
                     aux2['tarifa'][i]])
    # base
    base = folium.Map([y, x], zoom_start=11, tiles='OpenStreetMap')
    # adiciona heatmap a base
    HeatMap(aux3, name="Média da Tarifa diária mensal",gradient={'0':'Navy', '0.25':'Blue','0.5':'Green', '0.75':'Yellow','1': 'Red'}).add_to(base)
    # layer
    folium.LayerControl('topleft', collapsed= True).add_to(base)
    #plota heatmap
    with c2:
        folium_static(base)

    return None


def overview_price(data3, data):
    st.title('Análise econômica')
    st.header('Período Dez/2022 - Dez/2023')

    st.markdown('**Bairros com maiores taxa de ocupação**')
    #taxa de ocupacao
    df0 =( data3[['cidade','bairro','qtd_imoveis_bairro','qtd_anuncios_ano','qtd_diarias_anual','media_tax_mensal']]
             .sort_values('media_tax_mensal',ascending=False).head()) 
    st.dataframe(df0)
    
    # tarifa diaria media ocupacao mensal
    st.markdown('**Bairros com maiores tarifas diárias média mensal de ocupação**')
    df0 = ( data3[['cidade','bairro','qtd_imoveis_bairro','qtd_anuncios_ano','qtd_diarias_anual','media_tdm_oc_mes']]
             .sort_values('media_tdm_oc_mes',ascending=False).head())
    st.dataframe( df0.style.format( {'media_tdm_oc_mes': 'R${:,.2f}'} ))
    # faturamento
    st.markdown('**Bairros com maiores faturamentos**')
    df0 = ( data3[['cidade','bairro','qtd_imoveis_bairro','qtd_anuncios_ano','qtd_diarias_anual','fat_anual','fat/imovel','fat/diaria','fat/anuncio']]
             .sort_values('fat_anual',ascending=False).head() )
    st.dataframe(df0.style.format({'fat_anual': 'R${:,.2f}','fat/imovel': 'R${:,.2f}','fat/diaria': 'R${:,.2f}','fat/anuncio': 'R${:,.2f}'} ))
    # bairros selecionados
    st.header('Bairros Selecionados')
    st.markdown('**Critério:** Maiores taxa de ocupação / Maiores tarifas diárias média de ocupação mensal/ Maiores faturamentos anual') 
    st.markdown('**Bairros Selecionados:** Centro, Perequê, Meia Praia, Jardim Dourado, Tabuleiro dos Oliveiras')
    lista = ['Centro', 'Perequê', 'Meia Praia', 'Jardim Dourado', 'Tabuleiro dos Oliveiras']
    aux4 = data3.loc[data3['bairro'].isin(lista)]
    aux4 = aux4.drop('ano_add',axis=1)
    st.dataframe(aux4.style.format({'media_tax_mensal': '{:,.4f}','fat_anual': 'R${:,.2f}','fat/imovel': 'R${:,.2f}','fat/diaria': 'R${:,.2f}','fat/anuncio': 'R${:,.2f}','media_tdm_oc_mes': 'R${:,.2f}'} ))
    
    # analise bairros selecionados
    lista = ['Centro', 'Perequê', 'Meia Praia', 'Jardim Dourado', 'Tabuleiro dos Oliveiras']
    aux1 = data[['cidade', 'bairro', 'listing_type','number_of_bedrooms', 'number_of_beds', 'number_of_bathrooms','number_of_guests','garagem']]
    for i in lista:
        aux2 = aux1.loc[aux1['bairro']== i]
        st.markdown('**{}**'.format(i))
        #st.write(aux2.describe().T)
        df0 = aux2.describe().T
        st.dataframe(df0.style.format({'count':'{:.1f}','mean':'{:.2f}','std':'{:.2f}','min':'{:.2f}','25%':'{:.2f}','50%':'{:.2f}','75%':'{:.2f}','max':'{:.2f}'}))
        aux3 = aux2['listing_type'].value_counts(normalize = True).index.tolist()
        st.write('Tipo de imóvel mais frequente: ', aux3[0],round((aux2['listing_type'].value_counts(normalize = True)[0]*100),2),'%')
        aux3 = aux2['garagem'].value_counts(normalize = True).index.tolist()
        st.write('Possui garagem: ', aux3[0],round((aux2['garagem'].value_counts(normalize = True)[0]*100),2),'%')
    
    # perguntas de negocio
    st.header('Respondendo as perguntas de negócio')
    
    # pergunta 1
    st.markdown('**1. Qual o melhor perfil de imóvel para investir na cidade?**')
    st.write('O melhor perfil consiste em apartamentos com 3 quartos, 2 banheiros e com garagem.')
    # pergunta 2
    st.markdown('**2. Qual é a melhor localização na cidade em termos de receita?**')
    st.write('Imóveis localizados no bairro Centro de Itapema possuem a melhor localização em termos de receita.')
    # pergunta 3
    st.markdown('**3. Quais são as características e razões para as melhores receitas da cidade?**')
    st.write('Imóveis localizados no bairro Centro de Itapema possuem maiores faturamentos anual por imóvel, por anúncio e por diárias consolidadas.')
    st.write('Além disso, a tarifa diária média mensal ao longo do ano foi a maior entre os bairros.')
    st.write('Em termos de faturamento anual bruto, os 291 imóveis ficaram na segunda posição em volume.')
    st.write('O terceiro quartil dos imóveis localizados no Centro contemplam o perfil de apartamentos com 3 quartos, 2 banheiros e com garagem.')
    
    return None


if __name__ == '__main__':
    # data extration

    # paths e datas    
    path = './data/data_t3/df_unificado.csv'
    data = get_data(path)

    path2 = './data/data_t2/dataframe_bairros_2.csv'
    data2 = get_data2(path2)

    path3 = './data/data_t4/price.csv'
    data3 = get_data3(path3)

    path4 = './data/data_t2/shapes/municipios/itapema.shp'
    data4 = get_data4(path4)

    path5 = './data/data_t2/shapes/municipios/porto_belo.shp'
    data5 = get_data5(path5)

    path6 = './data/data_t2/shapes/municipios/balneario.shp'
    data6 = get_data6(path6)

    path7 = './data/data_t2/shapes/SC-DATASET/DATASET.shp'
    data7 = get_data7(path7)

    path8 = './data/data_t2/shapes/municipios/camboriu.shp'
    data8 = get_data8(path8)

    # transformation

    overview_data(data)

    portfolio_density(data2, data, data4,data5,data6,data7,data8)

    overview_price(data3, data)
