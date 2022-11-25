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
    donnees_pop_leg_19 = donnees_pop_leg_19.assign(CODGEO = donnees_pop_leg_19['CODDEP'] + donnees_pop_leg_19['CODCOM'])
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
    donnees_chomage_15_24_par_com_travail.rename(
        columns = {'codgeo':'CODGEO'}, inplace = True)
    donnees_chomage_15_24_par_com_travail = donnees_chomage_15_24_par_com_travail.set_index("CODGEO")

    
    return donnees_chomage_15_24_par_com_travail

def data_demandeurs_emploi():
    # url d'origine :
    # https://www.insee.fr/fr/statistiques/fichier/6473526/DEFM2021_iris.xlsx
    # https://www.insee.fr/fr/statistiques/6473526
    # permet d'avoir des données sur Paris et ses arrondissements, même si les demandeurs d'emploi ABC
    # ne sont pas exactement les chômeurs au sens du BIT
    # données en COG 2021
    """url_demandeurs_emploi = "https://www.insee.fr/fr/statistiques/fichier/6473526/DEFM2021_iris.xlsx"

    de_com = pd.read_excel(url_demandeurs_emploi, sheet_name='COM_2021', skiprows=5)

    de_com = de_com[['CODGEO', 'ABCDE','ABC']] #on pourrait venir en récupérer plus notamment les différences hommes femmes
    de_com.set_index("CODGEO", inplace=True, drop=True)"""

    url_demandeurs_emploi = "https://dares.travail-emploi.gouv.fr/sites/default/files/f49f1d0d9c5393de6efbf46b7be050c1/Dares_donnees-communales_demandeurs-demploi_2021.xlsx"

    de_com = pd.read_excel(url_demandeurs_emploi,
        sheet_name='ABC', skiprows=11)
    """de_com.rename(columns=['REG','LIBREG','DEP',
        'LIBDEP','CODGEO','communes',
        '2012','2013','2014',',2015','2016','2017','2018','2019',
        '2020','2021'])"""
    de_com.rename(columns={"Unnamed: 4":"CODGEO","Unnamed: 2":"DEP",2018:"de_ABC_2018"}, inplace=True)
    #le quatrimère trimestre 2018, on pourrait utilisé aussi le 4ème trimestre 2019

    #il faudrait faire le passage CODGEO2022 à CODGEO2021
    de_com['de_ABC_2018'].replace({'45*':45,'290*':290},
        inplace=True) # la donnée de la ville de Sannerville et Troarn
        # est entaché d'erreur, mais cela est minime
    de_com = de_com.astype({'de_ABC_2018':int})
    de_com.set_index("CODGEO", inplace=True)
    de_com = de_com[["de_ABC_2018"]]

    #on prend seulement la france métropolinaine

    return de_com


def trouve_commune_with_fuzz(donnees_cog_2021,libelle,dep):
    mondf=donnees_cog_2021[donnees_cog_2021['DEP']==dep]
    mondf['score']=mondf['NCC'].apply(lambda x: fuzz.token_sort_ratio(x,libelle))
    mondf=mondf.sort_values(by="score",ascending=False)
    return mondf['NCC et COM'].iloc[0]