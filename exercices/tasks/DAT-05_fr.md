# **DAT-05** / Suivre l'évolution du chiffre d'affaire de chacun des freelances


## Contexte
L'équipe Care a besoin de suivre l'évolution du chiffre d'affaire mois par mois des freelances : un chiffre d'affaire qui stagne n'est pas bon signe et il est nécessaire d'appeler le freelance pour comprendre sa situation.


## Action
Il faut réaliser un rapport avec la somme cumulée du chiffre d'affaire par mois et par freelance. Il faudrait pour cela avoir un tableau :
| Nom du freelance | Prénom du freelance | Date de début du CDI | Date de fin du CDI | Entité | Mois | Chiffre d'affaire (en €) |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| DUPOND | Albert | 2022/02/01 |  | blue | 2022/04 | 34,15 |
| DUPOND | Albert | 2022/02/01 |  | blue | 2022/05 | 67,15 |
| ... | ... | ... | ... | ... | ... | ... | ... |

idée:
import pandas as pd


df_contracts = pd.DataFrame(intermediate_contracts)
df_freelancers = pd.DataFrame(intermediate_freelancers)
df_invoices = pd.DataFrame(intermediate_invoices)

# Fusionner les données des contrats avec les données des freelances
df_merged = pd.merge(df_freelances, df_contracts, on='Nom du freelance', how='inner')

# Fusionner les données des factures avec les données fusionnées précédemment
df_merged = pd.merge(df_merged, df_invoices, on='Nom du freelance', how='inner')

# Calculer la somme cumulée du chiffre d'affaires par mois et par freelance
df_merged['Chiffre d\'affaire cumulé (en €)'] = df_merged.groupby(['Nom du freelance', 'Mois'])['Chiffre d\'affaire (en €)'].cumsum()

# Réorganiser les colonnes dans l'ordre souhaité
df_merged = df_merged[['Nom du freelance', 'Prénom du freelance', 'Date de début du CDI', 'Date de fin du CDI', 'Entité', 'Mois', 'Chiffre d\'affaire cumulé (en €)']]

# Afficher le résultat
print(df_merged)
