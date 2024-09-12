import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
import time
# Initialisation du contrôleur du clavier
keyboard = Controller()
# Création d'une liste des touches pour le clavier visuel
keys = [["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"],
        ["W", "X", "C", "V", "B", "N"]]
finalText = ""  # Variable pour stocker le texte tapé
displayedText = ""  # Variable pour le texte affiché
# Initialisation du détecteur de mains
detector = HandDetector(staticMode=False, maxHands=2, detectionCon=0.6)
# Ouverture de la capture vidéo
cap = cv2.VideoCapture(0)
# Définir la taille de la fenêtre (Largeur x Hauteur)
desired_width = 1280
desired_height = 960
# Contrôler la vitesse d'affichage des lettres
lastUpdateTime = time.time()
displayDelay = 0.5  # Délai de 0.5 seconde entre chaque lettre affichée
# Fonction pour dessiner le clavier visuel
def drawKeyboard(img, keys):
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            x = 100 * j + 50
            y = 100 * i + 50
            cv2.rectangle(img, (x, y), (x + 85, y + 85), (255, 0, 255), cv2.FILLED)
            cv2.putText(img, key, (x + 20, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img
# Fonction pour vérifier si un doigt touche une touche
def checkKeyPress(lmList, keys):
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            x = 100 * j + 50
            y = 100 * i + 50
            # Vérifier si l'index est sur la touche
            if x < lmList[8][0] < x + 85 and y < lmList[8][1] < y + 85:
                cv2.rectangle(img, (x, y), (x + 85, y + 85), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, key, (x + 20, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                return key  # Retourner la touche sélectionnée
    return None
def saveTextToFile(text):
    file_path = 'text.txt'
    # Ouvrir en mode append, créer le fichier s'il n'existe pas
    with open(file_path, 'a') as f:
        f.write(text + '\n')
while True:
    success, img = cap.read()
    # img = cv2.flip(img, 1)  # Retourner l'image pour que le mouvement soit plus naturel
    # Redimensionner l'image capturée à la taille de fenêtre souhaitée
    img = cv2.resize(img, (desired_width, desired_height))
    hands, img = detector.findHands(img, draw=True)  # Détection des mains
    # Dessiner le clavier visuel
    img = drawKeyboard(img, keys)
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        # Vérification si l'index appuie sur une touche
        pressedKey = checkKeyPress(lmList, keys)  # Capturer la touche appuyée directement
        if pressedKey:
            finalText += pressedKey  # Ajouter la touche capturée au texte
    # Ajouter une lettre à la fois au texte affiché avec un délai
    currentTime = time.time()
    if currentTime - lastUpdateTime > displayDelay and len(displayedText) < len(finalText):
        displayedText += finalText[len(displayedText)]
        lastUpdateTime = currentTime
    # Afficher le texte tapé au-dessous du clavier
    cv2.putText(img, displayedText, (50, 450), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)
    # Sauvegarder le texte dans le fichier après chaque nouvelle touche
    saveTextToFile(finalText)
    # Affichage de la fenêtre avec l'image
    cv2.imshow("Img", img)
    # Quitter avec 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()