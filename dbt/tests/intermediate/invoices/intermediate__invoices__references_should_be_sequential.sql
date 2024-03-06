{{ config(
    intermediate_invoices="invoices",
) }}


SELECT
    b.*
FROM
    {{ ref("intermediate__base__invoices") }} b


# Sélection des références de factures qui commencent par 'JMP'
query = select([invoices.c.reference]).where(invoices.c.reference.like('JMP%'))
result = engine.execute(query)

references = [int(row.reference[3:]) for row in result]  # Extraction du nombre de référence

# Vérification des trous dans la séquence des références
missing_references = []
for i in range(min(references), max(references)):
    if i not in references:
        missing_references.append(i)

# Affichage des références manquantes
if missing_references:
    print("Références manquantes détectées :", missing_references)
else:
    print("Aucune référence manquante détectée.")
