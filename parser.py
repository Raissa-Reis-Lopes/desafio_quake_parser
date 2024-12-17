# Para ler e procesar o log

import re
from collections import defaultdict

def parse_log(file_path):
    games = {}
    current_game = {}
    game_number = 0
    
    with open(file_path, 'r') as file:
        for line in file:
            # Identificar o início de uma nova partida
            if "InitGame" in line:
                if current_game:
                    games[f"game_{game_number}"] = current_game
                game_number += 1
                current_game = {"total_kills": 0, "players": set(), "kills": defaultdict(int), "kills_by_means": defaultdict(int)}
            
            # Contar kills
            if "Kill:" in line:
                current_game["total_kills"] += 1
                match = re.search(r"Kill: \d+ (\d+) (\d+): (.+) killed (.+) by (\w+)", line)
                
                if match:
                    killer_id, victim_id, killer, victim, death_cause = match.groups()
                    if killer == "<world>":
                        current_game["kills"][victim] -= 1
                    else:
                        current_game["kills"][killer] += 1
                        current_game["players"].add(killer)
                    current_game["players"].add(victim)
                    current_game["kills_by_means"][death_cause] += 1

        # Salvar o último jogo
        if current_game:
            games[f"game_{game_number}"] = current_game

    # Converter jogadores para lista
    for game in games.values():
        game["players"] = list(game["players"])
    
    return games
