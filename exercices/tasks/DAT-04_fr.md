# **DAT-04** / ⚠️ Il manque le mois d'octobre 2023 sur le chiffre d'affaire par mois !


## Contexte
Le KPI _Monthly Turnover_ est suivi par le CFO pour s'assurer de la santé de Jump.

Il se trouve qu'il a remarqué qu'il n'y avait pas de ligne pour Octobre 2023.


## Action
Il faut corriger ça en affichant tout de même une ligne pour ce mois malgré le fait qu'il n'y ait pas eu d'activité.


## Tips
1) Le _Monthly Turnover_ est calculé dans [ce fichier](../../dbt/models/marts/kpi/marts__kpi__monthly_turnover.sql)
2) Le package [dbt-utils](https://github.com/dbt-labs/dbt-utils) et sa fonction `date_spine` a été ajouté comme dépendence au projet 