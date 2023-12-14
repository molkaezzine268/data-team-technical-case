# Exercices

## Objectif

Tu trouveras ici la liste des tickets à réaliser dans le cadre du test technique qui fait parti du processus de recrutement chez Jump. 

Tu peux répondre comme cela te convient le mieux : 
* Tu peux forker le dépôt et faire une PR ;
* Envoyer un fichier ZIP avec les modifications que tu veux apporter ;
* ...Ou autre ! 

Bon courage !


## Tâches


### Tâche #01 - Séquentialité des références de facture

#### Contexte
L'équipe de comptabilité nous a rappelé qu'il fallait absolument que les références des factures se suivent : elle doivent suivre le pattern `JMPXXXXX` où `XXXXX` est un nombre (préfixé avec des `0` pour que la référence ait une taille fixe).


#### Action
Il faut créer un test de manière à s'assurer qu'il n'y a pas de trou au niveau des factures. Le test doit être au niveau `WARN` et ne pas mettre en péril l'alimentation de l'ensemble du Lakehouse.


#### Indices
1) Tu peux t'appuyer sur le modèle [`intermediate__invoices`](../dbt/models/intermediate/intermediate__invoices.sql) pour récupérer la liste des factures
2) Tu peux écrire ton test dans [ce fichier](../dbt/tests/intermediate/intermediate__invoice_references_should_be_sequential.sql)


### Tâche #02 - Calcul du NPS

#### Contexte
L'équipe de support a envoyé des sondages aux différents freelances pour recueillir un score de satisfaction. 
Ils aimeraient à présent avoir accès au [NPS](https://www.qualtrics.com/fr/gestion-de-l-experience/client/nps/) calculé à partir de ce score.

#### Action
Tu dois créer un model qui permet d'avoir accès à cet indicateur.

#### Indices
1) Le score de satisfaction est un entier qui se trouve dans la colonne `satisfaction_score` du modèle [`intermediate__freelances`](../dbt/models/intermediate/intermediate__freelances.sql#L11)
3) Tu peux écrire le model dans [ce fichier](../dbt/models/marts/kpi/marts__kpi_nps.sql)

> 💡 Les données ne sont pas historisées, c'est donc normal que tu n'aies en résultat qu'un nombre seul, sans aucune dimension.


### Tâche #03 - Analyse du chiffre d'affaire par cohort et par mois d'émission

### Tâche #04 - Bug sur le 