# Transformations

## Présentation

Ce dossier contient toutes les transformations nécessaires à l'alimentation des différentes couches du Lakehouse sous la forme d'un projet [DBT](https://www.getdbt.com/).

L'organisation suit [l'architecture en médaillon](https://www.databricks.com/fr/glossary/medallion-architecture) et [les préconisations de DBT](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview) : 
* La couche _Bronze_ correspond l'ensemble des modèles `staging` ;
* La couche _Silver_ à l'ensemble des modèles `intermediate`  ;
* Et la couche _Gold_ à l'ensemble des modèles `marts`.


## Utilisation

🚧 TODO
 - Ajouter la freshness (via une colonne `created_at` dans les CSV)
 - Ajouter un dummy profile pour pouvoir attaquer la base de données DuckDB directement