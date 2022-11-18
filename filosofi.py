"""
Fichier contenant les fonctions pour l'import, le cleaning et la visualisation des données issues de la base filosofi
réalisation : Charlotte Combier, Guilhem Sirot
"""

#Imports
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd 
import plotly.express as px

#Scrapping

def cog_2021():
    """le choix est fait de travailler en géographie de l'Insee 2021. """

    cog_commune = pynsee.download.telechargerDonnees("COG_COMMUNE", date = "dernier")
    URL_COG_2021="https://www.insee.fr/fr/statistiques/fichier/5057840/commune2021-csv.zip"

    #Télécharger le zip de l'URL
    r=requests.get(URL_COG_2021)

    open("commune2021-csv.zip", 'wb').write(r.content)


    with ZipFile("commune2021-csv.zip",'r') as myzip:
       data = myzip.open("commune2021.csv")

    donnees_cog_2021=pd.read_csv(data,dtype=str)
    # On enleve les communes associées,arrondissements et déléguées pour simplifier le dataframe
    donnees_cog_2021=donnees_cog_2021[~donnees_cog_2021.TYPECOM.isin(["COMA","COMD","ARM"])]
    donnees_cog_2021['NCC et DEP']= donnees_cog_2021['NCC'] + " " + donnees_cog_2021['DEP']
    donnees_cog_2021['NCC et COM']= donnees_cog_2021['NCC'] + " ," + donnees_cog_2021['COM']
    return donnes_cog_2021

def trouve_commune_with_fuzz(donnees_cog_2021,libelle,dep):
    mondf=donnees_cog_2021[donnees_cog_2021['DEP']==dep]
    mondf['score']=mondf['NCC'].apply(lambda x: fuzz.token_sort_ratio(x,libelle))
    mondf=mondf.sort_values(by="score",ascending=False)
    return mondf['NCC et COM'].iloc[0]

#Cleaning

#Visualisation

def asciiprint(variable,desc):
    print("-"*100)
    print(variable,":",desc)
    print("-"*100)

def showgraph(geometries,df,geometries_idf,df_idf,var,color,label):
    """ A compléter """
    asciiprint(var,label)
    fig, ax = plt.subplots(figsize=(10,10))

    geometries.plot(color='gray', ax=ax)
    df.plot(column=var, 
                        cmap=color, 
                        linewidth=0.5, 
                        edgecolor='black',
                        ax=ax, 
                        legend=True,
                        legend_kwds={'label': label, 'orientation': "horizontal"})
    ax.set_axis_off()
    
    fig, ax = plt.subplots(figsize=(10,10))

    geometries_idf.plot(color='gray', ax=ax)
    df_idf.plot(column=var, 
                        cmap=color, 
                        linewidth=0.5, 
                        edgecolor='black',
                        ax=ax, 
                        legend=True,
                        legend_kwds={'label': label, 'orientation': "horizontal"})
    ax.set_axis_off()
    
# Récupération des données des communes

def gpd_communes():
    """
    Récupération du polygone des communes
    """
    # Récupération de tous le fichier sur data.gouv
    url_com = 'https://www.data.gouv.fr/fr/datasets/r/61b8f19d-66ce-4ad3-a9c4-82502dc9d550'
    communes = gpd.read_file(url_com)
    #on ne veut que l'identifiant et la geometry
    communes = communes[["insee", "geometry"]]
    communes.columns = ["CODGEO", "geometry"]
    communes.set_index('CODGEO')
    
    # récupération du code départemental
    communes['dep'] = communes['CODGEO'].str[:2]
    communes['dep'] = communes['dep'].replace({'2A': 20})
    communes['dep'] = communes['dep'].replace({'2B': 20})
    communes['dep']  = pd.to_numeric(communes['dep'])
    
    # restriction à ma France métropolitaine
    communes = communes.loc[communes["dep"] <=95]
    return communes

def carte_communes_france_idf(geometries,df, var,color,label):
    # on crée une base pour var par faciliter
    df_var = df[var].to_frame()
    df_var.index.name = ['CODGEO'] 
    
    # on crée un df avec les données de var et les geometries
    carto_var=geometries.merge(df_var, how='left', on='CODGEO')
    carto_var.sort_values(by=['CODGEO'])
    #normalement les bases sont déjà filtrés à la France métropolitaine, mais par sécurité 
    carto_var['dep'] = carto_var['CODGEO'].str[:2]
    carto_var['dep'] = carto_var['dep'].replace({'2A': 20})
    carto_var['dep'] = carto_var['dep'].replace({'2B': 20})
    carto_var['dep']  = pd.to_numeric(carto_var['dep'])
    carto_var = carto_var.loc[carto_var["dep"] <=95]
    
    # création des geometries_idf et carto_var_idf
    carto_var_idf = carto_var.loc[carto_var['CODGEO'].str.slice(0, 2).isin(['75','77','78','91','92','93','94','95'])]
    
    showgraph(geometries,carto_var,geometries_idf,carto_var_idf,var,color,label)
