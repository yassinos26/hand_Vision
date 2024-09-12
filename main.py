import os
def run_keyboard_app():
    # Exécute le code du clavier virtuel
    os.system('python clavier.py')
def run_draw_app():
    # Exécute le code de dessin avec pinceau
    os.system('python draw.py')
def run_game_app():
    # Exécute le code du jeu Tic-Tac-Toe
    os.system('python game.py')
def main():
    while True:
        print("\n=== Menu Principal ===")
        print("1. Clavier virtuel")
        print("2. Dessin avec pinceau")
        print("3. Jeu Tic-Tac-Toe")
        print("4. Quitter")
        choice = input("Choisissez une option (1-4): ")
        if choice == '1':
            print("Lancement du clavier virtuel...")
            run_keyboard_app()
        elif choice == '2':
            print("Lancement du dessin avec pinceau...")
            run_draw_app()
        elif choice == '3':
            print("Lancement du jeu Tic-Tac-Toe...")
            run_game_app()
        elif choice == '4':
            print("Fermeture du programme.")
            break
        else:
            print("Option invalide. Veuillez choisir entre 1 et 4.")
if __name__ == "__main__":
    main()