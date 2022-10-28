### Python-data-2A-CMS
## Idée de projet :
1. Collecter sur le site des fédérations les coordonnées des clubs amateurs.
    - [Base de données de l’enquête nationale sur les pratiques physiques et sportives (ENPPS) de l’INJEP](https://www.data.gouv.fr/fr/datasets/donnees-geocodees-issues-du-recensement-des-licences-et-clubs-aupres-des-federations-sportives-agreees-par-le-ministere-charge-des-sports/), disponible sur data.gouv.fr, donne par sport et par ville le nombre de clubs et de licenciés. Attention encoding des fichiers en cp1250 !
    - [Base de données permanentes des équipements sportifs](https://equipements.sports.gouv.fr/api/v2/console), disponible par une [API ODSQL](https://help.opendatasoft.com/apis/ods-explore-v2/#section/Opendatasoft-Query-Language-(ODSQL)/Language-elements) permet d’avoir les coordonnées
    - [Base filosofi](https://www.insee.fr/fr/metadonnees/source/serie/s1172), données soci-économiques et la base [2019](https://www.insee.fr/fr/statistiques/6036907) disponibles par API ou pynsee. [Documentations sur les bases de données locales INSEE](https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=DonneesLocales&version=V0.1&provider=insee#!/default/getDonnees)
        - [Code géo](https://www.insee.fr/fr/information/3720946), [API Fichiers locaux](https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=DonneesLocales&version=V0.1&provider=insee#!/default/getDonnees), [version visuelle](https://www.insee.fr/fr/statistiques/6037462?geo=DEP-75)
2. Clean les données et premières visualisation (par exemple emplacements des 
équipements sportifs)
3. Modélisation : économétrique pas suffisante, machine learning. Que faire ?
    
## Critiques
1. Données
    - On n’a qu’une pratique « officielle », marquée par la licence : on peut rater d’autres pratiques moins formelles  
    - Si on se limite à regarder des données commune par commune ou département par département : on crée des barrière imaginaire => besoin d’avoir des distances => voir si RDD: peut être une opportunité
    - Quid du ML ? 
    - On est réduits à télécharger les données sur le site de l'Insee sans utiliser l'API car il est encore pas suffisament opérationnel pour être utile dans le cadre du projet  

## Choses à faire pour le traitement de données qui me viennent (CC) au fur et à mesure du travail: 

- supprimer les outre mer mais garder la corse (donc supprimer pour les codes geo sup ou égaux à 97)
- harmoniser le nom de toutes les variables correspondant au code commune insee et dénomer cette variable "CODGEO" par cohérence avec les codes pour les cartes ensuite
- traiter les NaN?
