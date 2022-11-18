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

#Cleaning

#Visualisation

def asciiprint(variable,desc):
    print("-"*100)
    print(variable,":",desc)
    print("-"*100)

def showgraph(departements,df,dep_idf,df_idf,var,color,label):
    asciiprint(var,label)
    fig, ax = plt.subplots(figsize=(10,10))

    departements.plot(color='gray', ax=ax)
    df.plot(column=var, 
                        cmap=color, 
                        linewidth=0.5, 
                        edgecolor='black',
                        ax=ax, 
                        legend=True,
                        legend_kwds={'label': label, 'orientation': "horizontal"})
    ax.set_axis_off()
    
    fig, ax = plt.subplots(figsize=(10,10))

    dep_idf.plot(color='gray', ax=ax)
    df_idf.plot(column=var, 
                        cmap=color, 
                        linewidth=0.5, 
                        edgecolor='black',
                        ax=ax, 
                        legend=True,
                        legend_kwds={'label': label, 'orientation': "horizontal"})
    ax.set_axis_off()