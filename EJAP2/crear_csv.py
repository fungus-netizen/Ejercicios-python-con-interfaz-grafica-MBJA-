import requests
import csv

# Queria probar apis y crear csv :D

def crear_csv(puuid, region, api_key, csv_path='match_data.csv', count=20):
    
    # Obtener lista de matches
    match_fetch = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&api_key={api_key}"
    match_list = requests.get(match_fetch).json()

    match_data_list = []
    
    # Procesar cada match
    for match_id in match_list:
        match_info_fetch = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
        match_info = requests.get(match_info_fetch).json()
        
        # Encontrar el participante con el puuid del usuario
        participant = None
        if 'info' in match_info and 'participants' in match_info['info']:
            for p in match_info['info']['participants']:
                if p.get('puuid') == puuid:
                    participant = p
                    break
        
        # Extraer datos del participante
        if participant and 'info' in match_info:
            # La base de la api separa informacion general del math  en "info" y la informacion del participante en "participants"
            # "challenges" es una tabla dentro de cada participante que contiene info adicional. Se toman las relevantes para el desempeño del jugador
            challenges = participant.get('challenges', {})
            
            match_data = {
                'match_id': match_id,
                'game_length': match_info['info'].get('gameDuration', ''),
                'tagline': participant.get('riotIdTagline', ''),
                'champion': participant.get('championName', ''),
                'spell1_casts': participant.get('spell1Casts', ''),
                'spell2_casts': participant.get('spell2Casts', ''),
                'spell3_casts': participant.get('spell3Casts', ''),
                'spell4_casts': participant.get('spell4Casts', ''),
                'level': participant.get('champLevel', ''),
                'kills': participant.get('kills', ''),
                'deaths': participant.get('deaths', ''),
                'assists': participant.get('assists', ''),
                'total_damage': participant.get('totalDamageDealtToChampions', ''),
                'damage_taken': participant.get('totalDamageTaken', ''),
                'gold_earned': participant.get('goldEarned', ''),
                'gold_spent': participant.get('goldSpent', ''),
                'gold_per_minute': challenges.get('goldPerMinute', ''),
                'bounty_gold': challenges.get('bountyGold', ''),
                'minions_killed': participant.get('totalMinionsKilled', ''),
                'wards_placed': participant.get('wardsPlaced', ''),
                'wards_killed': participant.get('wardsKilled', ''),
                'vision_score': participant.get('visionScore', ''),
                'turret_kills': participant.get('turretKills', ''),
                'turret_lost': participant.get('turretsLost', ''),
                'inhibitor_kills': participant.get('inhibitorKills', ''),
                'inhibitor_lost': participant.get('inhibitorsLost', ''),
                'nexus_kills': participant.get('nexusKills', ''),
                'nexus_lost': participant.get('nexusLost', ''),
                'win': participant.get('win', ''),
                'team': participant.get('teamId', ''),
                'lane': participant.get('lane', ''),
                'role': participant.get('role', ''),
                'team_position': participant.get('teamPosition', ''),
                'individual_position': participant.get('individualPosition', ''),
                'double_kills': participant.get('doubleKills', ''),
                'triple_kills': participant.get('tripleKills', ''),
                'quadra_kills': participant.get('quadraKills', ''),
                'penta_kills': participant.get('pentaKills', ''),
            }
            match_data_list.append(match_data)
    
    # Combinar datos existentes + nuevos
    full_match_list = match_data_list
    
    if full_match_list:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            # Escribir datos en el CSV
            writer = csv.DictWriter(f, fieldnames=full_match_list[0].keys()) # fieldnames -> Define las columnas del CSV
            # DictWriter -> Escribir diccionarios en el CSV
            writer.writeheader()
            writer.writerows(full_match_list)
    
    return len(match_data_list) # Retorna la cantidad de matches procesados y guardados en el CSV
