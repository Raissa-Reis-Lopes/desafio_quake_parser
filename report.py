def print_match_report(games):
    for game_name, data in games.items():
        print(f"{game_name}:")
        print(f"  Total de Kills: {data['total_kills']}")
        print(f"  Jogadores: {', '.join(data['players'])}")
        print("  Kills por jogador:")
        for player, kills in data["kills"].items():
            print(f"    {player}: {kills}")
        print("  Mortes por causa:")
        for cause, count in data["kills_by_means"].items():
            print(f"    {cause}: {count}")
        print("-" * 30)
