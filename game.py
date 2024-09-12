import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
# Initialisation du détecteur de mains
detector = HandDetector(staticMode=False, maxHands=2, detectionCon=0.7, minTrackCon=0.7)
# Variables du jeu
board = np.zeros((3, 3), dtype=int)  # Grille 3x3, vide au début
player_turn = 1  # 1 pour 'X', 2 pour 'O'
game_over = False
# Taille de la grille visuelle
grid_size = 600
cell_size = grid_size // 3
# Création de la fenêtre vidéo
cap = cv2.VideoCapture(0)
# Définir la taille de la fenêtre (Largeur x Hauteur)
desired_width = 1280
desired_height = 960
# Fonction pour dessiner la grille de jeu
def draw_grid(img):
    for i in range(1, 3):
        # Lignes verticales
        cv2.line(img, (i * cell_size, 0), (i * cell_size, grid_size), (255, 255, 255), 3)
        # Lignes horizontales
        cv2.line(img, (0, i * cell_size), (grid_size, i * cell_size), (255, 255, 255), 3)
# Fonction pour dessiner 'X' ou 'O' sur la grille
def draw_marks(img, board):
    for i in range(3):
        for j in range(3):
            center_x = j * cell_size + cell_size // 2
            center_y = i * cell_size + cell_size // 2
            if board[i, j] == 1:  # 'X'
                cv2.line(img, (j * cell_size + 20, i * cell_size + 20), ((j + 1) * cell_size - 20, (i + 1) * cell_size - 20), (0, 0, 255), 10)
                cv2.line(img, ((j + 1) * cell_size - 20, i * cell_size + 20), (j * cell_size + 20, (i + 1) * cell_size - 20), (0, 0, 255), 10)
            elif board[i, j] == 2:  # 'O'
                cv2.circle(img, (center_x, center_y), cell_size // 3, (255, 0, 0), 10)
# Fonction pour vérifier si un joueur a gagné
def check_winner(board):
    for i in range(3):
        if board[i, 0] == board[i, 1] == board[i, 2] != 0:  # Lignes horizontales
            return board[i, 0]
        if board[0, i] == board[1, i] == board[2, i] != 0:  # Lignes verticales
            return board[0, i]
    if board[0, 0] == board[1, 1] == board[2, 2] != 0:  # Diagonale principale
        return board[0, 0]
    if board[0, 2] == board[1, 1] == board[2, 0] != 0:  # Diagonale secondaire
        return board[0, 2]
    return 0  # Aucun gagnant pour l'instant
# Fonction pour placer un symbole dans la grille
def place_symbol(board, x, y, symbol):
    row = y // cell_size
    col = x // cell_size
    if board[row, col] == 0:  # Si la case est vide
        board[row, col] = symbol
        return True
    return False
while True:
    success, img = cap.read()
    img = cv2.resize(img, (desired_width, desired_height))
    hands, img = detector.findHands(img, draw=True)  # Détection des mains
    # Zone de jeu 300x300 pixels
    img_game = np.zeros((grid_size, grid_size, 3), dtype=np.uint8)
    draw_grid(img_game)  # Dessiner la grille
    draw_marks(img_game, board)  # Dessiner les symboles X et O
    if hands and not game_over:
        for hand in hands:
            lmList = hand['lmList']
            x, y = lmList[8][0], lmList[8][1]  # Position du doigt index
            # Vérifier si la main droite ou gauche contrôle le mouvement
            if hand['type'] == "Right":  # Main droite = 'O'
                if place_symbol(board, x, y, 2):
                    player_turn = 1  # Changer de tour
            elif hand['type'] == "Left":  # Main gauche = 'X'
                if place_symbol(board, x, y, 1):
                    player_turn = 2  # Changer de tour
    # Vérification du gagnant
    winner = check_winner(board)
    if winner != 0:
        game_over = True
        cv2.putText(img_game, f"Player {winner} wins!", (50, grid_size // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # Afficher la zone de jeu
    img[0:grid_size, 0:grid_size] = img_game
    # Affichage de la fenêtreq
    cv2.imshow("Tic-Tac-Toe", img)
    # Quitter le jeu avec 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()