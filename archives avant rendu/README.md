# Python-data-2A-CMS
# Analyses de l'influence des pratiques sportives à partir de données socio-économiques.
## Bases utilisées
- [Base de données de l’enquête nationale sur les pratiques physiques et sportives (ENPPS) de l’INJEP](https://www.data.gouv.fr/fr/datasets/donnees-geocodees-issues-du-recensement-des-licences-et-clubs-aupres-des-federations-sportives-agreees-par-le-ministere-charge-des-sports/), disponible sur data.gouv.fr, donne par sport et par ville le nombre de clubs et de licenciés. Attention encoding des fichiers en cp1250 !
- [Base de données permanentes des équipements sportifs](https://equipements.sports.gouv.fr/api/v2/console), disponible par une [API ODSQL](https://help.opendatasoft.com/apis/ods-explore-v2/#section/Opendatasoft-Query-Language-(ODSQL)/Language-elements) permet d’avoir les coordonnées
- [Base filosofi](https://www.insee.fr/fr/metadonnees/source/serie/s1172), données soci-économiques et la base [2019](https://www.insee.fr/fr/statistiques/6036907) disponibles par API ou pynsee. [Documentations sur les bases de données locales INSEE](https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=DonneesLocales&version=V0.1&provider=insee#!/default/getDonnees)
- [Code géo](https://www.insee.fr/fr/information/3720946), [API Fichiers locaux](https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=DonneesLocales&version=V0.1&provider=insee#!/default/getDonnees), [version visuelle](https://www.insee.fr/fr/statistiques/6037462?geo=DEP-75)
- Données de chômage et des demandeurs d'emplois (DARES)

## Actions réalisées :
1. Cleaning et filtration sur la France métropolitaine
2. Agrégations des bases et éjection d'outliers
3. Visualisation par des cartes
4. Clustering sur les pratiques sportives
5. Prédiction/classification de ces clusters par des données socio-économiques
    
## Pré-critiques
- On n’a qu’une pratique « officielle », marquée par la licence : on peut rater d’autres pratiques moins formelles  
- On regarde les données communes par communes ce qui créé des barrières imaginaire
