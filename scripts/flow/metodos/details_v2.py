# imports
import pandas as pd
import logging
import os

# functions

def loading_data(path):
    df = pd.read_csv(path)
    
    return df

def data_cleaning(data):

    df1 = data.copy()
    
    # fill na's
    
    # ad_description 6 % - host didn't fill
    df1['ad_description'] = df1['ad_description'].fillna('no_description')
    
    # space                        0.47
    df1['space'] = df1['space'].fillna('no_description')
    
    # house_rules                  0.09
    df1['house_rules'] = df1['house_rules'].fillna('no_description')
    
    # number_of_bathrooms 
    df1['number_of_bathrooms'] = df1.apply(lambda x: 1 if x['ad_id']==          30153564 else x['number_of_bathrooms'], axis = 1)
    
    df1['number_of_bathrooms'] = df1.apply(lambda x: 3 if x['ad_id']==           53774942 else x['number_of_bathrooms'], axis = 1)
    
    df1['number_of_bathrooms'] = df1.apply(lambda x: 1 if x['ad_id']== 563923122447968990 else x['number_of_bathrooms'], axis = 1)
    
    df1['number_of_bathrooms'] = df1.apply(lambda x: 2 if x['ad_id']==           53173167 else x['number_of_bathrooms'], axis = 1)
    
    # number_of_bedrooms           0.02 fill with 1 studio ou quarto - erro
    df1['number_of_bedrooms'] = df1['number_of_bedrooms'].fillna(1.0)
    
    # number_of_beds               0.01
    df1['number_of_beds'] = df1.apply(lambda x: 2  if x['ad_id']== 41271947 else x['number_of_bathrooms'], axis = 1)
    df1['number_of_beds'] = df1.apply(lambda x: 3  if x['ad_id']== 41813666 else x['number_of_bathrooms'], axis = 1)
    df1['number_of_beds'] = df1.apply(lambda x: 10 if x['ad_id']== 49369605 else x['number_of_bathrooms'], axis = 1)
    df1['number_of_beds'] = df1.apply(lambda x: 1  if x['ad_id']== 46370376 else x['number_of_bathrooms'], axis = 1)
    df1['number_of_beds'] = df1.apply(lambda x: 2  if x['ad_id']== 41266511 else x['number_of_bathrooms'], axis = 1)
    df1['number_of_beds'] = df1.apply(lambda x: 1  if x['ad_id']== 47754124 else x['number_of_bathrooms'], axis = 1)
    df1['number_of_beds'] = df1.apply(lambda x: 2  if x['ad_id']== 50097179 else x['number_of_bathrooms'], axis = 1)
    df1['number_of_beds'] = df1.apply(lambda x: 4  if x['ad_id']== 40759616 else x['number_of_bathrooms'], axis = 1)
    df1['number_of_beds'] = df1.apply(lambda x: 3  if x['ad_id']== 41721914 else x['number_of_bathrooms'], axis = 1)
    df1['number_of_beds'] = df1.apply(lambda x: 3  if x['ad_id']== 41008210 else x['number_of_bathrooms'], axis = 1)
    # df1['number_of_beds'] = df1.apply(lambda x: 3  if x['ad_id']== 45899764 else x['number_of_bathrooms'], axis = 1)
    
    # star_rating                  0.48
    df1['star_rating'] = df1.apply(lambda x: 5  if (x['ad_id']== 31055581) and (x['star_rating'] == 0.0 )else x['star_rating'], axis = 1)
    
    df1['star_rating'] = df1['star_rating'].fillna(0.0)
    
    # additional_house_rules       0.57
    df1['additional_house_rules'] = df1['additional_house_rules'].fillna('no_description')
    
    # check_in                     0.08
    df1['check_in'] = df1.apply( lambda x: 'Flexível' if ( pd.isnull(x['check_in']) ) & (pd.notna(x['check_out']) ) else x['check_in'], axis = 1)
    df1['check_in'] = df1['check_in'].fillna('no_description')
    
    # check_out                    0.21
    df1['check_out'] = df1.apply( lambda x: 'Flexível' if ( pd.isnull(x['check_out']) ) & (pd.notna(x['check_in']) ) else x['check_out'], axis = 1)
    df1['check_out'] = df1['check_out'].fillna('no_description')
    
    # cohosts                      0.87
    df1['cohosts'] = df1['cohosts'].fillna('no_cohost')
    
    # index                        0.73
    df1['index'] = df1['index'].fillna(1)
    
    # localized_star_rating        0.48
    df1['localized_star_rating'] = df1['localized_star_rating'].fillna(0)
    
    # response_time_shown          0.90
    df1['response_time_shown'] = df1['response_time_shown'].fillna('no_description')
    
    # response_rate_shown          0.90
    df1['response_rate_shown'] = df1['response_rate_shown'].fillna('111%')
    
    # guest_satisfaction_overall   0.91
    df1['guest_satisfaction_overall'] = df1['guest_satisfaction_overall'].fillna(111)
    
    # picture_count                0.87
    df1['picture_count'] = df1['picture_count'].fillna(200)
    
    # min_nights                   0.87
    df1['min_nights'] = df1['min_nights'].fillna(0)
    
    #logger.debug('quantidade de nan"s\n%s', df1.isna().sum() )
    
    # change Types

    # aquisition_date                object
    df1['aquisition_date'] = pd.to_datetime(df1['aquisition_date'])
    
    # number_of_bathrooms           float64
    df1['number_of_bathrooms'] = df1['number_of_bathrooms'].astype(int)
    
    # number_of_bedrooms            float64
    df1['number_of_bedrooms'] = df1['number_of_bedrooms'].astype(int)
    
    # number_of_beds                float64
    df1['number_of_beds'] = df1['number_of_beds'].astype(int)
    
    # is_superhost                     bool
    df1['is_superhost'] = df1['is_superhost'].apply(lambda x: 0 if (x == False) else 1)
    
    # localized_star_rating          object
    df1['localized_star_rating'] = df1['localized_star_rating'].str.replace(',','.')
    
    df1['localized_star_rating'] = df1['localized_star_rating'].astype(float)
    
    
    df1['localized_star_rating'] = df1['localized_star_rating'].fillna(0.0)
    
    # guest_satisfaction_overall    float64
    df1['guest_satisfaction_overall'] = df1['guest_satisfaction_overall'].astype(int)
    
    # picture_count                 float64
    df1['picture_count'] = df1['picture_count'].astype(int)
    
    # min_nights                    float64
    df1['min_nights'] = df1['min_nights'].astype(int)
    
    # feature engineering
    
    # house rules
    aux12 = ['Animais de estimação são permitidos',
             'Não permite animais de estimação',
             'Não são permitidas festas ou eventos',
             'Não é adequado para bebês (menores de 2 anos)',
             'Não é adequado para crianças de 2 a 12 anos',
             'Não é adequado para crianças ou bebês',
             'Proibido fumar',
             'Self check-in com equipe do edifício',
             'Self check-in com fechadura inteligente',
             'Self check-in com lockbox',
             'Self check-in com teclado com senha',
             'É permitido fumar']
    
    df1['house_rules_new'] = ''
    for i in range (len(df1['house_rules'])):
        lista=[]
        for j in aux12:
            if j in df1.loc[i,'house_rules']:
                lista.append(j)
        df1['house_rules_new'].loc[i] = lista
        
    df1[['house_rules','house_rules_new']].head()
    df1['house_rules_new'] = df1['house_rules_new'].apply(lambda x: ','.join(x) )
    df1['house_rules']     = df1['house_rules_new'].copy()
    
    
    # amenities
    aux12 = ['Academia','Acesso ao lago','Alarme de monóxido de carbono','Aquecimento Central','Ar-condicionado','Assadeira',
             'Babá eletrônica','Banheira','Banheira de bebê','Berço','Bicicletas','Bidê','Blackout nas cortinas','Básico',
             'Cabides','Cadeira alta','Cafeteira','Cafeteira Keurig','Cafeteira com coador','Café da Manhã','Caiaque',
             'Carregador de veículos elétricos','Casa térrea','Cercadinho/berço portátil','Chaleira de água quente',
             'Churrasqueira','Chuveiro externo','Cobertores e travesseiros extras','Cofre','Condicionador','Conexão à Ethernet',
             'Console de video game','Cozinha','Detector de fumaça','Elevador','Entrada privada','Entrada/saída para esquis',
             'Espaço de trabalho exclusivo','Estacionamento gratuito na rua','Estacionamento incluído',
             'Estacionamento pago fora da propriedade','Estacionamento pago no local','Estadias de longa duração são permitidas',
             'Extintor de incêndio','Fechadura inteligente','Ferro de passar','Fogueira','Fogão','Forno','Freezer','Frigobar',
             'Funcionários do edifício','Gel de banho','Itens básicos de cozinha','Itens básicos de praia','Jacuzzi',
             'Jogos de tabuleiro','Kit de primeiros socorros','Kitchenette','Lareira interna','Lava-louças',
             'Lavanderia nas proximidades','Limpeza antes do checkout','Livros e brinquedos infantis','Lixeira compactadora',
             'Local para guardar as roupas','Louças e talheres','Mesa de bilhar','Mesa de jantar','Mesa de ping pong',
             'Microondas','Mosquiteiro','Máquina de Lavar','Máquina de café espresso','Máquina de pão','Móveis externos',
             'O anfitrião recebe você','Panela elétrica de arroz','Piano','Piscina','Portões de segurança para bebês',
             'Pratos e talheres para crianças','Produtos de limpeza','Protetores de cantos de mesa','Protetores de lareira',
             'Protetores de tomada','Pátio ou varanda','Quintal','Rampa para barcos','Recomendações de babás',
             'Rede/grade de proteção nas janelas','Refrigerador','Roupa de cama','Sabonete para o corpo','Sauna',
             'Secador de cabelo','Secadora','Sistema de som','TV','TV a Cabo','Taças de vinho','Teclado numérico',
             'Toca-discos','Torradeira','Tranca na porta do quarto','Trocador','Utensílios para churrasco',
             'Varal para secar roupas','Ventilador de teto','Ventiladores portáteis','Vista para as águas',
             'Vista para o mar','Wi-Fi','Wifi portátil','Xampu','Água quente','Área de jantar externa',
             'É permitido deixar as malas']
    
    df1['amenities_new'] = ''
    for i in range (len(df1['amenities'])):
        lista=[]
        for j in aux12:
            if j in df1.loc[i,'amenities']:
                lista.append(j)
        df1['amenities_new'].loc[i] = lista
        
    df1['amenities_new'] = df1['amenities_new'].apply(lambda x: ','.join(x) )
    df1['amenities']     = df1['amenities_new'].copy()
    
    # safety_features
    aux12 = ['Alarme de monóxido de carbono','Detector de fumaça','Extintor de incêndio','Kit de primeiros socorros',
             'Tranca na porta do quarto']
    
    df1['safety_features_new'] = ''
    for i in range (len(df1['safety_features'])):
        lista=[]
        for j in aux12:
            if j in df1.loc[i,'safety_features']:
                lista.append(j)
        df1['safety_features_new'].loc[i] = lista
    
    df1['safety_features_new'] = df1['safety_features_new'].apply(lambda x: ','.join(x) )
    df1['safety_features']     = df1['safety_features_new'].copy()
    df1['safety_features']     = df1['safety_features'].apply(lambda x: 'no_description' if x == '' else x)
    
    # listing_type
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Quarto inteiro em casa' if x == 'Quarto inteiro em casa particular' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Quarto inteiro em casa' if x == 'Quarto inteiro em casa na terra' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Quarto inteiro em casa' if x == 'Quarto inteiro em microcasa' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Quarto inteiro em casa' if x == 'Quarto inteiro em townhouse' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Espaço inteiro: casa' if x == 'Casa na terra' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Espaço inteiro: casa' if x == 'Casa particular' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Espaço inteiro: casa' if x == 'Espaço inteiro: casa de veraneio' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Espaço inteiro: casa' if x == 'Espaço inteiro: bangalô' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Espaço inteiro: casa' if x == 'Espaço inteiro: vila' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Quarto inteiro em apartamento' if x == 'Quarto inteiro em condomínio' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Quarto inteiro em apartamento' if x == 'Quarto inteiro em suíte de hóspedes' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Espaço inteiro: apartamento' if x == 'O lugar inteiro' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Espaço inteiro: apartamento' if x == 'Casa/apto inteiro' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Espaço inteiro: apartamento' if x == 'Quarto em apart-hotel' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Espaço inteiro: loft' if x == 'Microcasa' else x)
    df1['listing_type'] = df1['listing_type'].apply(lambda x: 'Espaço inteiro: loft' if x == 'Microcasa' else x)
    
    
    df1['listing_type'] = df1.apply(lambda x: 'Contêiner de transporte' if x['ad_id'] == 40121694 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Contêiner de transporte' if x['ad_id'] == 52536959 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Espaço inteiro: casa' if x['ad_id'] == 753705661776365934 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Espaço inteiro: casa' if x['ad_id'] == 719608035919549657 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Espaço inteiro: chalé' if x['ad_id'] == 38327538 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Espaço inteiro: apartamento' if x['ad_id'] == 583188146814735405 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Espaço inteiro: apartamento' if x['ad_id'] == 640011391336388796 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Espaço inteiro: apartamento' if x['ad_id'] == 762192750283483456 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Espaço inteiro: loft' if x['ad_id'] == 759586614872722965 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Quarto inteiro em pousada' if x['ad_id'] == 39701557 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Quarto inteiro em pousada' if x['ad_id'] == 31055188 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Quarto inteiro em pousada' if x['ad_id'] == 50052580 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Quarto inteiro em pousada' if x['ad_id'] == 650592591360054871 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Quarto inteiro em casa' if x['ad_id'] == 21479549 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Quarto inteiro em casa' if x['ad_id'] == 639626077681798500 else x['listing_type'], axis = 1)
    df1['listing_type'] = df1.apply(lambda x: 'Quarto inteiro em casa' if x['ad_id'] == 546588792290672978 else x['listing_type'], axis = 1)
    
    
    # rating to category
    df1['localized_star_rating_cat'] = pd.cut( df1['localized_star_rating'], bins =[-0.005, 3.0, 3.5,4.0,4.5,5], labels = ['no_rating','low','medium','high','very_high'] )
    
    # estacionamento
    df1['garagem'] = df1.apply(lambda x: 'sim' if 'Estacionamento incluído' in x['amenities'] else 'nao', axis = 1)

    # filtering 
    df1['aquisition_date'] = pd.to_datetime(df1['aquisition_date'])
    df1['aquisition_date'] = df1['aquisition_date'].dt.strftime('%Y-%m-%d')
    
    aux1 = df1[['ad_id','aquisition_date']].groupby('ad_id').max().reset_index()
    
    aux1 = aux1.set_index('ad_id').T.to_dict('list')
    
    df1['aquisition_date_max'] = df1['ad_id'].map(aux1)
    
    df1['aquisition_date_max'] = df1['aquisition_date_max'].apply(lambda x: ','.join(x) )
    
    df1['aquisition_date_max'] = df1['aquisition_date_max'].astype('category')
    
    df1['check'] = df1.apply(lambda x: True if x['aquisition_date']==x['aquisition_date_max'] else False, axis = 1)
    
    df1 = df1.loc[df1['check']==True].copy()
    
    df1 = df1.drop_duplicates()
    
    df1['house_rules'] = df1['house_rules'].fillna('no_description')

    df1['amenities']   = df1['amenities'].fillna('no_description')
    
    df1['house_rules_new'] = df1['house_rules_new'].fillna('no_description')

    df1['amenities_new']   = df1['amenities_new'].fillna('no_description')
    
   
    return df1
            
def save_csv(data,path,name):   
    aux1 = path+name
    data.to_csv(aux1, index = False)
    
    return None
