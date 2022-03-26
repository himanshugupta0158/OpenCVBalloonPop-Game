# Import
import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time

# Initialize
pygame.init()

# Create Window/Display
width , height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")

# Initialize Clock for FPS(Frame Per Seconds)
fps = 30
clock = pygame.time.Clock()

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3,1280) # width
cap.set(4,720) # height


# Images
imgBalloon = pygame.image.load("BalloonRed.png")
rectBalloon = imgBalloon.get_rect()
rectBalloon.x , rectBalloon.y = 500,300

# variables
speed = 15
score = 0
startTime = time.time()


def resetBalloon():
    rectBalloon.x = random.randint(100,img.shape[1]-100)
    rectBalloon.y = img.shape[0]+50
    

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)


# Main Loop
start = True

while start :
    # Get events
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
            
        
    # Applying Logic
    timeRemain = int(time.time() - startTime)
    
    # OpenCV
    success , img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    
    rectBalloon.y -= speed
    
    if rectBalloon.y < 0 :
        resetBalloon()
        speed += 1
    if hands :
        # hand = hands[0]
        dimension=hands[0]["lmList"][8]
        if rectBalloon.collidepoint(dimension[0],dimension[1]) :
            resetBalloon()
            speed += 1
            score += 10
            
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame,True,False)
    window.blit(frame, (0,0))
    
    window.blit(imgBalloon, rectBalloon)
    
    font = pygame.font.Font('Marcellus-Regular.ttf',50)
    textScore = font.render(f'Score : {score}', True , (50,50,200))
    textTime = font.render(f'Time : {timeRemain}', True , (50,50,200))
    window.blit(textScore, (35,35))
    window.blit(textTime, (1000, 35))
    
    
    
    # Update Display
    pygame.display.update()
    
    # Set FPS
    clock.tick(fps)
    
    
