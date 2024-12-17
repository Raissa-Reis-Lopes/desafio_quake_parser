from parser import parse_log
from report import print_match_report
import os

def print_menu():
    print("\n===== MENU DE RELATÓRIOS =====")
    print("1 - Relatório Completo (Todos os jogos)")
    print("2 - Relatório de um Jogo Específico")
    print("3 - Relatório de Jogos sem Mortes")
    print("4 - Relatório de Kills por Jogador")
    print("5 - Relatório de Jogos Ordenados por Número de Kills")
    print("6 - Salvar Relatório Completo em Arquivo de Texto")
    print("7 - Sair")
    print("==============================")

def report_specific_game(games):
    print("\nJogos disponíveis:")
    for game_name in games.keys():
        print(f" - {game_name}")
    game_choice = input("Digite o nome do jogo (ex: game_1): ").strip()
    if game_choice in games:
        print(f"\nRelatório para {game_choice}:")
        print_match_report({game_choice: games[game_choice]})
    else:
        print("Jogo não encontrado! Tente novamente.")

def report_games_without_kills(games):
    print("\nRelatório de Jogos sem Mortes:")
    no_kill_games = {name: data for name, data in games.items() if data['total_kills'] == 0}
    if no_kill_games:
        print_match_report(no_kill_games)
    else:
        print("Não existem jogos sem mortes.")

def report_kills_by_player(games):
    print("\nRelatório de Kills por Jogador:")
    player_kills = {}
    for game in games.values():
        for player, kills in game["kills"].items():
            player_kills[player] = player_kills.get(player, 0) + kills
    
    if player_kills:
        for player, kills in sorted(player_kills.items(), key=lambda x: x[1], reverse=True):
            print(f"{player}: {kills} kills")
    else:
        print("Não foram encontrados registros de kills.")

def report_games_sorted_by_kills(games):
    print("\nRelatório de Jogos Ordenados por Número de Kills:")
    sorted_games = sorted(games.items(), key=lambda x: x[1]["total_kills"], reverse=True)
    for game_name, data in sorted_games:
        print(f"{game_name}: {data['total_kills']} kills")

def save_report_to_file(games):
    file_name = input("Digite o nome do arquivo (ex: relatorio.txt): ").strip()
    with open(file_name, "w") as file:
        for game_name, data in games.items():
            file.write(f"{game_name}:\n")
            file.write(f"  Total de Kills: {data['total_kills']}\n")
            file.write(f"  Jogadores: {', '.join(data['players'])}\n")
            file.write("  Kills por jogador:\n")
            for player, kills in data["kills"].items():
                file.write(f"    {player}: {kills}\n")
            file.write("  Mortes por causa:\n")
            for cause, count in data["kills_by_means"].items():
                file.write(f"    {cause}: {count}\n")
            file.write("-" * 30 + "\n")
    print(f"Relatório salvo com sucesso em '{file_name}'.")

if __name__ == "__main__":
    log_path = "logs/qgames.log"
    
    # Verificar se o arquivo de log existe
    if not os.path.exists(log_path):
        print("Arquivo de log não encontrado! Verifique o caminho.")
        exit()
    
    # Parsear o log
    games = parse_log(log_path)

    while True:
        print_menu()
        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            print("\nRelatório Completo:")
            print_match_report(games)
        elif choice == "2":
            report_specific_game(games)
        elif choice == "3":
            report_games_without_kills(games)
        elif choice == "4":
            report_kills_by_player(games)
        elif choice == "5":
            report_games_sorted_by_kills(games)
        elif choice == "6":
            save_report_to_file(games)
        elif choice == "7":
            print("Saindo do programa. Até logo!")
            break
        else:
            print("Opção inválida! Tente novamente.")
