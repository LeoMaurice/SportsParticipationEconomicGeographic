import requests
import pandas as pd

import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA
from mpl_toolkits.axes_grid1 import host_subplot

def licence_club():
    url_licence = 'https://static.data.gouv.fr/resources/donnees-geocodees-issues-du-recensement-des-licences-et-clubs-aupres-des-federations-sportives-agreees-par-le-ministere-charge-des-sports/20220823-100513/lic-data-2019.csv'
    file_licence = url_licence.split('/')[-1] #encoding de ce fichier 'cp1250'
    url_club = 'https://static.data.gouv.fr/resources/donnees-geocodees-issues-du-recensement-des-licences-et-clubs-aupres-des-federations-sportives-agreees-par-le-ministere-charge-des-sports/20220519-175014/clubs-data-2019.csv'
    file_club = url_club.split('/')[-1]

    licence = pd.read_csv(url_licence, header = 0, encoding = 'cp1250', sep=';', low_memory=False)
    club = pd.read_csv(url_club, header = 0, encoding = 'cp1250', sep=';', low_memory=False)
    return licence, club

def test_encoding(file):
    """
    Les fichiers issues de l'enquête sportive sont dans un encoding unusuel.
    On met en place une fonction pour tester tous les encoding
    Cependant il y a besoin d'un contrôle visuel car certains encodings peuvent ouvrir mais en comprenant mal certains caractères typiques du français
    
    A priori pour executer le code on a pas besoin de cette fonction mais permet d'expliquer comment
    on a trouvé cp1250
    """
    codecs = ['cp1250','ascii','big5','big5hkscs','cp037','cp273','cp424','cp437','cp500','cp720','cp737','cp775','cp850','cp852','cp855',
          'cp856','cp857','cp858','cp860','cp861','cp862','cp863','cp864','cp865','cp866','cp869','cp874','cp875','cp932','cp949',
          'cp950','cp1006','cp1026','cp1125','cp1140','cp1250','cp1251','cp1252','cp1253','cp1254','cp1255','cp1256','cp1257','cp1258',
          'euc_jp','euc_jis_2004','euc_jisx0213','euc_kr','gb2312','gbk','gb18030','hz','iso2022_jp','iso2022_jp_1','iso2022_jp_2',
          'iso2022_jp_2004','iso2022_jp_3','iso2022_jp_ext','iso2022_kr','latin_1','iso8859_2','iso8859_3','iso8859_4','iso8859_5','iso8859_6',
          'iso8859_7','iso8859_8','iso8859_9','iso8859_10','iso8859_11','iso8859_13','iso8859_14','iso8859_15','iso8859_16','johab','koi8_r','koi8_t',
          'koi8_u','kz1048','mac_cyrillic','mac_greek','mac_iceland','mac_latin2','mac_roman','mac_turkish','ptcp154','shift_jis','shift_jis_2004',
          'shift_jisx0213','utf_32','utf_32_be','utf_32_le','utf_16','utf_16_be','utf_16_le','utf_7','utf_8','utf_8_sig']


    for x in range(len(codecs)):
        print(x,': Now checking use of:', codecs[x])
        try:
            df = pd.read_csv(file, header = 0, encoding = (codecs[x]), sep=';')
            print(df.head())
            print(input('Press any key...'))
        except:
            print('I can\'t load data for', codecs[x], '\n')
            print(input('Press any key...'))

def get_es(url):
    """fonction qui a pour but à partir d'une URL de request de transformer en dataframe utilisable"""

    req = requests.get(url)
    wb = req.json()
    #print(wb)
    df = pd.json_normalize(wb)

    return df

def compte_commune_equip(equipements):
    # liste des familles
    familles = equipements['famille'].unique()

    #on crée une base par code geographique avec le total des infrastructures par commune
    base_equip_commune = equipements.groupby(['CODGEO']).count()
    # on regroupe par communes
    base_equip_commune.rename(columns={'commune':"total"}, inplace = True) #commune correspond au total
    base_equip_commune.dropna(inplace= True)
    base_equip_commune = base_equip_commune[['total']]
    # on vient compléter cette base du total des infrastructures

    # On ajout le nombre d'infrastructure par commune selon des critères d'accessibilité :
    critere_info = ["accesibilite_handicap", 'acces_libre']
    for info in critere_info:
        equipements[info].replace({'true':1,'false':0}, inplace = True) # on remplace les strings
    # equivalent à des bools par leurs indicatrices pour sommer
        base_equip_commune[info] = equipements.groupby(['CODGEO']).sum()[info]
        # la somme nous donne le total de équipements accessibles par commune selon les différents
        # critères d'accessibilités

    # puis on vient ajouter pour chaque famille d'équipement le nombre
    # en mettant 0 pour les villes n'en possédant pas
    temp = equipements.groupby(['famille','CODGEO']).count()   
    for fam in familles :
        base_equip_commune[fam] = temp.loc[fam]['commune']
    # pour la matrice CODGEO X famille, quand une famille est manquante
    # on obtiens un NaN, qu'on remplace par 0 car la traduction est ici l'absence de la famille dans la commune
    base_equip_commune.fillna(0, inplace = True) 

    base_equip_commune = base_equip_commune.astype(dtype=int)

    return base_equip_commune