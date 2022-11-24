"""
Fichier contenant les fonctions pour l'import, le cleaning et la visualisation des données issues de la base filosofi
réalisation : Charlotte Combier, Guilhem Sirot
"""

#Imports

# library carte

import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
from IPython.core.display import display, HTML

# Importation des librairies classiques de python
import unicodedata
import requests
import time
import os
from tqdm import tqdm
import io
import warnings

# Importation des librairies de datascience et autres
import pandas as pd
import numpy as np
import pynsee
import pynsee.download
from pynsee.sirene import *
from pynsee.utils.init_conn import init_conn
from zipfile import ZipFile
from fuzzywuzzy import fuzz
import cartiflette.s3
from cartiflette.download import get_vectorfile_ign

#Scrapping

def cog_2021():
    """le choix est fait de travailler en géographie de l'Insee 2021.
    On télécharge en direct depuis le site de l'INSEE à l'url :
    https://www.insee.fr/fr/statistiques/fichier/5057840/commune2021-csv.zip
    On aurait pu faire avec la bibliothèque pyinsee et l'api
    
    La fonction retourne un dataframe des codes géographiques 2021
    """
    # tentative avec l'API insee et pyinsee
    # cog_commune = pynsee.download.telechargerDonnees("COG_COMMUNE", date = "dernier")
    
    # téléchargement direct
    URL_COG_2021 = "https://www.insee.fr/fr/statistiques/fichier/5057840/commune2021-csv.zip"

    #Télécharger le zip de l'URL
    r=requests.get(URL_COG_2021)

    open("commune2021-csv.zip", 'wb').write(r.content)


    with ZipFile("commune2021-csv.zip",'r') as myzip:
        data = myzip.open("commune2021.csv")

    donnees_cog_2021 = pd.read_csv(data,dtype=str)
    # On enleve les communes associées,arrondissements et déléguées pour simplifier le dataframe
    donnees_cog_2021 = donnees_cog_2021[~donnees_cog_2021.TYPECOM.isin(["COMA","COMD","ARM"])]
    donnees_cog_2021['NCC et DEP'] = donnees_cog_2021['NCC'] + " " + donnees_cog_2021['DEP']
    donnees_cog_2021['NCC et COM'] = donnees_cog_2021['NCC'] + " ," + donnees_cog_2021['COM']
    return donnees_cog_2021


def filosofi_2019():
    """ Téléchargement direct des données filosofi depuis 
    URL de la page à télécharger : https://www.insee.fr/fr/statistiques/6036902
    La fonction retourne un dataframe des données filosofi 2019 et un dataframe de la table de variables"""
    
    # téléchargement
    
    URL_FILO_ZIP_2019="https://www.insee.fr/fr/statistiques/fichier/6036902/base-cc-filosofi-2019_CSV.zip"
    nom = URL_FILO_ZIP_2019.split('/')[-1]
    response=requests.get(URL_FILO_ZIP_2019)
    if response.status_code == 200:
            with open(nom, 'wb') as f:
                f.write(response.content)
    with ZipFile(nom, 'r') as zipfile :
        nom_fichier_data = "cc_filosofi_2019_COM.csv"
        nom_fichier_meta = "meta_"+nom_fichier_data
        data = zipfile.open(nom_fichier_data)
        meta = zipfile.open(nom_fichier_meta)
    donnees_filo_ind_communes_2019=pd.read_csv(data, sep=";", low_memory=False) 
    table_var_filo_ind_com_2019 = pd.read_csv(meta, sep=";", low_memory=False)   
    
    #cleaning
    
    donnees_filo_ind_communes_2019[['MED19','TP6019','RD19']] = donnees_filo_ind_communes_2019[['MED19','TP6019','RD19']].replace({'s':np.NaN})
    donnees_filo_ind_communes_2019[['TP6019','RD19']] = donnees_filo_ind_communes_2019[['TP6019','RD19']].apply(lambda x: x.str.replace(',', '.'))
    donnees_filo_ind_communes_2019 = donnees_filo_ind_communes_2019.astype({'MED19':float, 'TP6019':float,'RD19':float})
    
    return donnees_filo_ind_communes_2019, table_var_filo_ind_com_2019

def pop_2019():
    """Téléchargement des populations légales du millénisme 2018 
    La fonction retourne un dataframe des données de population légales du millénisme 2018"""
    # téléchargement
    
    URL_POP_LEG="https://www.insee.fr/fr/statistiques/fichier/6011070/ensemble.zip"

    #Télécharger le zip de l'URL
    r=requests.get(URL_POP_LEG)

    open("ensemble.zip", 'wb').write(r.content)


    with ZipFile("ensemble.zip",'r') as myzip:
        data = myzip.open("donnees_communes.csv")

    donnees_pop_leg_19=pd.read_csv(data,sep=';',dtype=str)
    
    #cleaning
    
    donnees_pop_leg_19["CODE_INSEE"]=donnees_pop_leg_19["CODDEP"]+donnees_pop_leg_19["CODCOM"]
    donnees_pop_leg_19=donnees_pop_leg_19.set_index("CODE_INSEE")
    donnees_pop_leg_19 = donnees_pop_leg_19.assign(codgeo = donnees_pop_leg_19['CODDEP'] + donnees_pop_leg_19['CODCOM'])
    donnees_pop_leg_19['PTOT'] = donnees_pop_leg_19['PTOT'].astype({'PTOT':float})
    
    return donnees_pop_leg_19
    
def data_chomage():
    """ Téléchargement des données de chomage directement depuis l'observatoire des territoires
    La fonction retourne un dataframe des données de chomage par commune de 2018"""
    
    # téléchargement
    
    
    URL_TAUX_CHOMAGE_15_24_PAR_COM="https://www.observatoire-des-territoires.gouv.fr/outils/cartographie-interactive/api/v1/functions/GC_API_download.php?type=stat&nivgeo=com2021&dataset=indic_sex_rp&indic=tx_chom1524"

    donnees_chomage_15_24_par_com=pd.read_excel(URL_TAUX_CHOMAGE_15_24_PAR_COM, sheet_name='Data',skiprows=4)
    
    donnees_chomage_15_24_par_com_travail = donnees_chomage_15_24_par_com[donnees_chomage_15_24_par_com["an"]==2018]
    donnees_chomage_15_24_par_com_travail = donnees_chomage_15_24_par_com_travail[donnees_chomage_15_24_par_com_travail["sexe"]=="T"]
    donnees_chomage_15_24_par_com_travail = donnees_chomage_15_24_par_com_travail.set_index("codgeo")
    
    return donnees_chomage_15_24_par_com_travail


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
                        linewidth=0.1, 
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
    # ancienne version
    #url_com = 'https://www.data.gouv.fr/fr/datasets/r/61b8f19d-66ce-4ad3-a9c4-82502dc9d550'
    #communes = gpd.read_file(url_com)

    communes = france = get_vectorfile_ign(
    level = "COMMUNE",
    field = "metropole",
    year = 2021)
    #source = "COG_EXPRESS",
    #provider="IGN")

    #projection
    communes = communes.to_crs(3857)

    #on ne veut que l'identifiant, le département et la geometry
    #communes = communes[["insee", "geometry"]] quand téléchargement via data.gouv
    communes = communes[["INSEE_COM","INSEE_DEP", "geometry"]]
    communes.columns = ["CODGEO","dep", "geometry"]
    communes.set_index('CODGEO', drop = False)

    arrondissements = cartiflette.s3.download_vectorfile_url_all(
        values = "75",
        level="ARRONDISSEMENT_MUNICIPAL",
        vectorfile_format="geojson",
        decoupage="departement",
        year=2022)

    arrondissements = arrondissements.to_crs(3857)

    arrondissements = arrondissements[["INSEE_ARM","INSEE_DEP", "geometry"]]
    arrondissements.columns = ["CODGEO","dep", "geometry"]
    arrondissements.set_index('CODGEO', drop = False)
    
    #division de paris en ces arrondissements
    communes = pd.concat(
    [
        communes[communes['dep'] != "75"],
        arrondissements
    ])
    
    # récupération du code départemental, méthode pour les données de data.gouv
    #communes['DEP'] = communes['CODGEO'].str[:2]

    #mise en numérique de la corse
    communes['DEP'] = communes['DEP'].replace({'2A': 20})
    communes['DEP'] = communes['DEP'].replace({'2B': 20})
    communes['DEP']  = pd.to_numeric(communes['DEP'])
    
    # restriction à ma France métropolitaine
    communes = communes.loc[communes["DEP"] <=95] #normalement c'est déjà le cas avec cartiflette mais redondance

    

    #projection
    return communes


def carte_communes_france_idf(geometries, df, var,color,label):
    # on crée une base pour var par faciliter
    
    df_var = df[var]

    # on crée un df avec les données de var et les geometries
    carto_var=geometries.merge(df_var, how='left', on='CODGEO')
    carto_var.sort_values(by=['CODGEO'])
    #normalement les bases sont déjà filtrés à la France métropolitaine, mais par sécurité 
    carto_var = ajout_dep(carto_var, 'CODGEO','DEP')
    carto_var = carto_var.loc[carto_var["DEP"] <=95]
    
    # création des geometries_idf et carto_var_idf
    carto_var_idf = carto_var.loc[carto_var['CODGEO'].str.slice(0, 2).isin(['75','77','78','91','92','93','94','95'])]

    geometries_idf = geometries.loc[geometries['DEP'].isin([75,77,78,91,92,93,94,95])]

    
    showgraph(geometries,carto_var,geometries_idf,carto_var_idf,var,color,label)

def carte_france_idf(geometries, df, var,color,label):
    # on crée une base pour var par faciliter
    
    df_var = df[var]

    # on crée un df avec les données de var et les geometries
    carto_var=geometries.merge(df_var, how='left', on='CODGEO')
    carto_var.sort_values(by=['CODGEO'])
    #normalement les bases sont déjà filtrés à la France métropolitaine, mais par sécurité 
    carto_var = ajout_dep(carto_var, 'CODGEO','DEP')
    carto_var = carto_var.loc[carto_var["DEP"] <=95]
    
    # création des geometries_idf et carto_var_idf
    carto_var_idf = carto_var.loc[carto_var['CODGEO'].str.slice(0, 2).isin(['75','77','78','91','92','93','94','95'])]

    geometries_idf = geometries.loc[geometries['DEP'].isin([75,77,78,91,92,93,94,95])]

    
    showgraph(geometries,carto_var,geometries_idf,carto_var_idf,var,color,label)


def ajout_dep(df, codgeo, dep):
    df[dep] = df[codgeo].str[:2]
    df[dep] = df[dep].replace({'2A': 20})
    df[dep] = df[dep].replace({'2B': 20})
    df[dep]  = pd.to_numeric(df[dep])
    return df
def ajout_paris_agrege(df, codgeo, dep):
    df[df[dep]==75]