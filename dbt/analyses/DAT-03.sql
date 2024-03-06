import pandas as pd

# Chargement des données des freelances depuis la table intermediate__freelances
df_freelances = pd.read_sql_query("SELECT * FROM intermediate__freelances;")

# Chargement des données des contrats depuis la table intermediate__job_contracts
df_contracts = pd.read_sql_query("SELECT * FROM intermediate__job_contracts;")

# Chargement des données des factures depuis la table intermediate__invoices
df_invoices = pd.read_sql_query("SELECT * FROM intermediate__invoices;")

# Fusionner les données des contrats avec les données des freelances
df_merged = pd.merge(df_freelances, df_contracts, left_on='sk', right_on='freelance_sk', how='inner')

# Fusionner les données des factures avec les données fusionnées précédemment
df_merged = pd.merge(df_merged, df_invoices, on='freelance_sk', how='left')

# Remplacer les valeurs NaN dans la colonne 'revenue_eur' par 0
df_merged['revenue_eur'].fillna(0, inplace=True)

# Renommer les colonnes pour correspondre à la demande du commissaire aux compte
df_merged.rename(columns={'last_name': 'Nom du freelance',
                           'first_name': 'Prénom du freelance',
                           'cohort': 'Cohort',
                           'entity': 'Entité',
                           'month': 'Mois',
                           'revenue_eur': 'Chiffre d\'affaire (en €)'}, inplace=True)

# Trier les données par Cohort, puis par Mois
df_merged.sort_values(by=['Cohort', 'Mois'], inplace=True)

# Réorganiser les colonnes dans l'ordre souhaité
df_merged = df_merged[['Nom du freelance', 'Prénom du freelance', 'Cohort', 'Entité', 'Mois', 'Chiffre d\'affaire (en €)']]

# Afficher le résultat
print(df_merged)
