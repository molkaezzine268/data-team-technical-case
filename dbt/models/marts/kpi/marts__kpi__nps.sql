{{ config(
    alias="freelances",
) }}


SELECT
    b.sk, 
    b.last_name,
    b.first_name,
    b.email,
    b.satisfaction_score
FROM
    {{ ref("intermediate__base__freelances") }} b


# Fonction pour calculer le NPS
def calculate_nps(b):
    # Nombre total de réponses
    total_responses = len(b)
    
    # Nombre de promoteurs (score 9 ou 10)
    promoters = b[b['satisfaction_score'] >= 9]
    num_promoters = len(promoters)
    
    # Nombre de détracteurs (score de 6 ou moins)
    detractors = b[b['satisfaction_score'] <= 6]
    num_detractors = len(detractors)
    
    # Calcul du NPS
    nps = (num_promoters - num_detractors) / total_responses * 100
    
    return nps

# Calcul du NPS à partir du DataFrame des scores de satisfaction
nps = calculate_nps(intermediate__base__freelances)

print("Le Net Promoter Score (NPS) est :", nps)
