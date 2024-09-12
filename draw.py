import cv2
from cvzone.HandTrackingModule import HandDetector
# Initialisation du détecteur de mains
detector = HandDetector(staticMode=False, maxHands=2, detectionCon=0.6)
# Ouverture de la capture vidéo
cap = cv2.VideoCapture(0)
# Définir la taille de la fenêtre (Largeur x Hauteur)
desired_width = 1280
desired_height = 960
# Définir les dimensions de la zone de dessin
draw_area_x = 50
draw_area_y = 50
draw_area_width = 500
draw_area_height = 500
# Variables pour le dessin avec le pinceau
brush_color = (0, 0, 255)  # Rouge pour le pinceau
brush_thickness = 10  # Taille du pinceau
brush_position = (0, 0)  # Position du pinceau
# Créer une image noire pour la zone de dessin
drawing_area = None
# Fonction pour dessiner la zone de dessin avec un fond noir
def draw_drawing_area(img):
    global drawing_area
    if drawing_area is None:
        drawing_area = img[draw_area_y:draw_area_y + draw_area_height, draw_area_x:draw_area_x + draw_area_width]
        drawing_area[:] = (0, 0, 0)  # Remplir la zone de dessin avec du noir
    else:
        img[draw_area_y:draw_area_y + draw_area_height, draw_area_x:draw_area_x + draw_area_width] = drawing_area
# Fonction de dessin avec le pinceau
def draw_brush(img, position):
    global brush_thickness, brush_color
    # Calculer les coordonnées du pinceau dans la zone de dessin
    x = position[0] - draw_area_x
    y = position[1] - draw_area_y
    # Vérifier si la position du pinceau est à l'intérieur de la zone de dessin
    if (0 <= x < draw_area_width and 0 <= y < draw_area_height):
        # Dessiner sur la zone de dessin
        cv2.circle(drawing_area, (x, y), brush_thickness, brush_color, -1)
while True:
    success, img = cap.read()
    # img = cv2.flip(img, 1)  # Retourner l'image pour que le mouvement soit plus naturel
    # Redimensionner l'image capturée à la taille de fenêtre souhaitée
    img = cv2.resize(img, (desired_width, desired_height))
    # Détection des mains
    hands, img = detector.findHands(img, draw=True)  
    # Dessiner la zone de dessin avec un fond noir
    draw_drawing_area(img)
    if hands:
        for hand in hands:
            lmList = hand['lmList']
            # Si la main est à droite
            if hand['type'] == 'Right':
                # Prendre la position de l'index (2ème doigt)
                brush_position = (lmList[8][0], lmList[8][1])
                # Dessiner à la position de l'index uniquement si dans la zone de dessin
                draw_brush(img, brush_position)
    # Affichage de la fenêtre avec l'image
    cv2.imshow("Img", img)
    # Quitter avec 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()