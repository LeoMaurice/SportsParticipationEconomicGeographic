# Examining the Relationship Between Economic and Geographic Factors and Participation in Sports Activities at the City Level.

Projet python réalisé à l'occasion d'un diplôme d'ingénieur à l'ENSAE.
Administrateurs stagiaires ayant travaillé sur le projet :
- Charlotte Combier
- Léopold Maurice
- Guilhem Sirot
# Analyses de l'influence des pratiques sportives à partir de données socio-économiques.
## Bases utilisées
- [Base de données de l’enquête nationale sur les pratiques physiques et sportives (ENPPS) de l’INJEP](https://www.data.gouv.fr/fr/datasets/donnees-geocodees-issues-du-recensement-des-licences-et-clubs-aupres-des-federations-sportives-agreees-par-le-ministere-charge-des-sports/), disponible sur data.gouv.fr, donne par sport et par ville le nombre de clubs et de licenciés. Attention encoding des fichiers en cp1250 !
- [Base de données permanentes des équipements sportifs](https://equipements.sports.gouv.fr/api/v2/console), disponible par une [API ODSQL](https://help.opendatasoft.com/apis/ods-explore-v2/#section/Opendatasoft-Query-Language-(ODSQL)/Language-elements)
- [Base filosofi](https://www.insee.fr/fr/metadonnees/source/serie/s1172), données socio-économiques et base [2019](https://www.insee.fr/fr/statistiques/6036907) disponibles par API ou pynsee. [Documentations sur les bases de données locales INSEE](https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=DonneesLocales&version=V0.1&provider=insee#!/default/getDonnees)
- [Code géo](https://www.insee.fr/fr/information/3720946), [API Fichiers locaux](https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=DonneesLocales&version=V0.1&provider=insee#!/default/getDonnees), [version visuelle](https://www.insee.fr/fr/statistiques/6037462?geo=DEP-75)
- [Données de demandeurs d'emploi de catégories ABC](https://www.insee.fr/fr/statistiques/6473526) (DARES)

## Organisation du repository

Le dossiers helpers contient 3 petits fichiers .py de fonctions d'aides pour ne pas encombrer le rendu jupyter. Ce dernier contient l'ensemble des actions : téléchargement, visualisation des données, puis modélisation et interprétations.

Un fichier requirements.txt permet d'installation les packages nécessaires si le jupyter lui même n'installe pas ce qu'il faut (normalement un bloc installation a été prévu. Ce bloc ne s'exécute que si : installations_needed = True).

Le lancement total de rendu est de : 20 mn dont les 3/4 dans le téléchargement et la création de cartes pour visualiser les données. Si on souhaite juste les données et les modèles, on peut utiliser au tout début VERBOSE = False pour ne pas avoir de graphiques ni de sortie et réduire ainsi le temps de rendu.

Par commodité on a supprimé l'essentiel de l'aléa sur le clustering pour faciliter la cohérence entre commentaires et résultats mais ces derniers sont cohérents qu'importe la seed.


## Actions réalisées :
1. Récupération des bases de données depuis internet par différentes façons (API, package python, lien direct)
2. Cleaning et filtration des données sur la France métropolitaine
3. Agrégations des bases et éjection d'outliers
4. Visualisation par des cartes
5. Réalisation de statistiques descriptives et de corrélations.
6. Clustering sur les pratiques sportives
7. Prédiction/classification de ces clusters par des données socio-économiques
8. Interprétations de ces clusters en tant que groupes de distinction culturelle et économique.
    
## Pré-critiques
- Notre étude ne s'attache qu'à une pratique « officielle », marquée par la licence : d’autres pratiques, moins formelles, ne sont pas étudiées.  
- Les données sont étudiées commune par commune, ce qui créé des barrières imaginaires : une pratique sportive peut avoir un sens seulement à une échelle multi communes.
- La partie de modélisation et de classification (actions 6 à 8) se limite au domaine urbain en n'étudiant que les villes de taille moyenne.
