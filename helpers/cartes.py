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
    communes.columns = ["CODGEO","DEP", "geometry"]
    communes.set_index('CODGEO', drop = False)

    arrondissements = cartiflette.s3.download_vectorfile_url_all(
        values = "75",
        level="ARRONDISSEMENT_MUNICIPAL",
        vectorfile_format="geojson",
        decoupage="departement",
        year=2022)

    arrondissements = arrondissements.to_crs(3857)

    arrondissements = arrondissements[["INSEE_ARM","INSEE_DEP", "geometry"]]
    arrondissements.columns = ["CODGEO","DEP", "geometry"]
    arrondissements.set_index('CODGEO', drop = False)
    
    #division de paris en ces arrondissements
    communes = pd.concat(
    [
        communes[communes['DEP'] != "75"],
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
    print("entrée ajout dep")
    df[dep] = df[codgeo].str[:2]
    df[dep] = df[dep].replace({'2A': 20})
    df[dep] = df[dep].replace({'2B': 20})
    df[dep]  = pd.to_numeric(df[dep])
    print("avant sortie ajout dep")
    return df