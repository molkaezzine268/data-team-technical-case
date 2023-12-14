# Data Platform

## Présentation globale

Ce dépôt contient l'ensemble du code qui constitue la Data Platform. La Data Platform constitue **l'ensemble des moyens techniques mis en oeuvre pour répondre aux besoins qui nécessitent l'exploitation de la donnée chez Jump** (rapports et dashboards, extractions ad-hoc, etc.) 

[!TIP]  
> Test

La clé de voute de la Data Platform est le Lakehouse : c'est une base de donnée analytique qui est composée de 4 couches :
* La couche Sources qui contient une copie de **l'ensemble des données brutes** issue des applications utilisées chez Jump (l'application dévelopée par les équipes Backend et Frontend, le CRM administré par l'équipe Sales, etc.)
* La couche Staging qui est très similaire à la couche précédente mais contient **quelques étapes de nettoyage, de filtrage**, etc. ;
* La couche Intermediate qui s'appuie sur la couche précédente et contient **un modèle homogène et cohérent qui couvre l'ensemble du périmètre fonctionnel** adressé par Jump (facturation, CDI des salariés portés, etc.) ;
* Le couche Marts qui contient **des modèles plus complexes mais à forte valeur ajoutée** nécessaires pour répondre à des besoins fonctionnels plus poussés. 

![Schéma](docs/schema.png)


## Implémentation technique

La Data Platform s'appuie sur les technologies suivantes : 
* Le Lakehouse est **une base de données [DuckDB](https://duckdb.org/)** :
    * Le fichier se trouve dans `./data/lakehouse/lakehouse.duckdb`, 
    * Chacune des couches logiques citées ci-dessus est un schéma ;
* L'ensemble des transformations est réalisé **à l'aide de [DBT](https://www.getdbt.com/)** grâce à [ce projet](./dbt/) ;
* Une [CLI](./cli) en Python (nommée `data-platform`) qui orchestre les différentes étapes d'alimentation de la Data Platform :
    * L'étape `extract` pour copier les données depuis les applications sous forme de base de données [SQLite](https://www.sqlite.org/index.html) dans le dossier `./data/sources`, 
    * L'étape `load` pour charger les données extraites dans le schéma `sources` du Lakehouse (qui va aller se trouver dans `./data/lakehouse`), 
    * L'étape `transform` pour alimenter les schémas `staging`, `intermediate` et `marts`.

L'ensemble est conteneurisé à l'aide de Docker et de [ce Dockerfile](./docker/Dockerfile).


## Utilisation

### Pré-requis
* Docker
* Make

### Commandes
* `make build` : construit l'image Docker qui embarque la CLI, le projet DBT, etc.
* `make extract` : lance l'extract des données de l'application et du CRM
* `make load` : lance l'inégration des extractions dans le schéma `source` du Lakehouse
* `make transform` : transforme les données et alimente les schémas `staging`, `intermediate` et `bronze` (à l'aide du [projet DBT](./dbt/))