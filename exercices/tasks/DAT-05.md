# **DAT-04** / Suivre l'évolution du chiffre d'affaire de chacun des freelances


## Contexte
L'équipe Care a besoin de suivre l'évolution du chiffre d'affaire mois par mois des freelances : un chiffre d'affaire qui stagne n'est pas bon signe et il est nécessaire d'appeler le freelance pour comprendre sa situation.


## Action
Il faut réaliser un rapport avec la somme cumulée du chiffre d'affaire par mois et par freelance. Il faudrait pour cela avoir un tableau :
| Nom du freelance | Prénom du freelance | Date de début du CDI | Date de fin du CDI | Entité | Mois | Chiffre d'affaire (en €) |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| DUPOND | Albert | 2022/02/01 |  | blue | 2022/04 | 34,15 |
| DUPOND | Albert | 2022/02/01 |  | blue | 2022/05 | 67,15 |
| ... | ... | ... | ... | ... | ... | ... | ... |


## Tips
1) Le _Monthly Turnover_ est calculé dans [ce fichier](../../dbt/models/marts/kpi/marts__kpi__monthly_turnover.sql)
2) Le package [dbt-utils](https://github.com/dbt-labs/dbt-utils) et sa fonction `date_spine` a été ajouté comme dépendence au projet 