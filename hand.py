import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp

# We are using pycaw for the volume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()
# Min and Max volume
minVol = volRange[0]
maxVol = volRange[1]

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

def draw_text_boxes(img):
    """Draw text boxes with specific labels on the frame."""
    labels = ["write", "daw", "play", "exit"]
    positions = [(50, 50), (50, 100), (50, 150), (50, 200)]
    for label, position in zip(labels, positions):
        cv2.putText(img, label, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

# Continuously get frames from the webcam
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=True, flipType=True)
    
    # Draw the text boxes on the frame
    draw_text_boxes(img)
    
    if hands:
        hand1 = hands[0]  # Get the first hand detected
        lmList1 = hand1["lmList"]  # (x,y,z) List of 21 landmarks for the first hand
        bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
        center1 = hand1['center']  # Center coordinates of the first hand
        handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")
        tipOfIndexFinger = lmList1[8][0:2]
        tipOfThumbFinger = lmList1[4][0:2]
        
        # Calculate distance between specific landmarks on the first hand and draw it on the image
        length, info, img = detector.findDistance(tipOfIndexFinger, tipOfThumbFinger, img, color=(255, 0, 255), scale=5)
        
        # Hand range 5 - 200
        # Volume range -65 - 0
        vol = np.interp(length, [20, 165], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)
    
    # Display the image in a window
    cv2.imshow("Image", img)
    
    # Keep the window open and update it for each frame; wait for 1 millisecond between frames
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
