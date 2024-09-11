import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import pygame
import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# Initialiser Pygame
pygame.init()
# Configuration du volume (pycaw)
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
# Configuration caméra
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Détecteur de mains
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

# Création de la fenêtre Pygame
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Main Menu")

# Variables de menu
font = pygame.font.Font(None, 36)
menu_items = ["write", "draw", "play", "exit"]
selected_item = None

def draw_text_boxes():
    """Dessine les boîtes de texte avec des étiquettes spécifiques dans la fenêtre Pygame."""
    y = 50
    for item in menu_items:
        label = font.render(item, True, (0, 255, 0))
        screen.blit(label, (50, y))
        y += 100

def open_virtual_keyboard():
    """Affiche un clavier virtuel."""
    print("Ouverture du clavier virtuel")
    # Ici, vous pouvez implémenter l'affichage d'un vrai clavier virtuel.

def open_draw_window():
    """Affiche la fenêtre de dessin."""
    print("Ouverture de la fenêtre de dessin")
    # Implémentez une interface de dessin simple.

def open_xoxo_game():
    """Affiche la fenêtre du jeu XOXO (tic-tac-toe)."""
    print("Lancement du jeu XOXO")
    # Implémentez une version simple du jeu tic-tac-toe.

# Main loop
running = True
while running:
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=True, flipType=True)
    
    # Interactions avec Pygame
    screen.fill((0, 0, 0))  # Remplir l'écran en noir
    draw_text_boxes()

    if hands:
        hand1 = hands[0]  # Première main détectée
        lmList1 = hand1["lmList"]  # Liste des landmarks de la première main
        tipOfIndexFinger = lmList1[8][0:2]
        tipOfThumbFinger = lmList1[4][0:2]
        
        # Calculer la distance entre l'index et le pouce
        length, info, img = detector.findDistance(tipOfIndexFinger, tipOfThumbFinger, img, color=(255, 0, 255), scale=5)
        vol = np.interp(length, [20, 165], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)
    
    # Détection des actions sur les éléments du menu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 50 <= y <= 150:
                selected_item = "Write"
                open_virtual_keyboard()
            elif 150 <= y <= 250:
                selected_item = "Draw"
                open_draw_window()
            elif 250 <= y <= 350:
                selected_item = "Play"
                open_xoxo_game()
            elif 350 <= y <= 450:
                selected_item = "Exit"
                running = False

    # Affichage des images et de la fenêtre Pygame
    pygame.display.update()
    cv2.imshow("Hand Detection", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()