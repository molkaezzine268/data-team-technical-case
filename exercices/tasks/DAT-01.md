# **DAT-01** / Vérifier la séquentialité des factures

## Contexte
L'équipe de comptabilité nous a rappelé qu'il fallait absolument que les références des factures se suivent : elle doivent suivre le pattern `JMPXXXXX` où `XXXXX` est un nombre (préfixé avec des `0` pour que la référence ait une taille fixe).


## Action
Il faut créer un test de manière à s'assurer qu'il n'y a pas de trou au niveau des factures. Le test doit être au niveau `WARN` et ne pas mettre en péril l'alimentation de l'ensemble du Lakehouse.


## Tips
1) Tu peux t'appuyer sur la colonne `reference` du modèle [`intermediate__invoices`](../../dbt/models/intermediate/intermediate__invoices.sql) pour récupérer la liste des références
2) Tu peux écrire ton test dans [ce fichier](../../dbt/tests/intermediate/intermediate__invoice_references_should_be_sequential.sql)


