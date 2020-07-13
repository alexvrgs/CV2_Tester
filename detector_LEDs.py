import cv2
import numpy as np
import ctypes
from time import *
import os


def pathVerification():
    global FolderName
    global path

    FolderName = "C:/Python/LED_Test/"
    path = strftime('%m_%d_%H_%M')
    Folderpath = FolderName + path

    if not os.path.exists(FolderName):
        print(f"Creating folder: {FolderName}")
        os.makedirs(FolderName)

    if not os.path.exists(Folderpath):
        print(f"Creating folder: {Folderpath}")
        os.makedirs(Folderpath)

def takeFrame():
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, "Presione 'OK' para iniciar la prueba", 'LED Test', 0)

    Camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while Camera.isOpened():
        ret, frame = Camera.read()
        if ret is not True: break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        k = cv2.waitKey(1)
        if k == 27: break

        cv2.imshow('Video', gray)
        cv2.imwrite(Folderpath + '/frame.bmp', gray)

    Camera.release()
    cv2.destroyAllWindows()

def drawCnt(contorno, color):
    for (c) in contorno:
        x, y, w, h = cv2.boundingRect(c)
        cv2.drawContours(imagen, [c], 0, color, 1)

def Inspection():
    Backup = "C:/Python/LED_Test/" + path +"Backup/"
    
    if not os.path.exists(Backup):
        print(f"Creating folder: {Backup}")
        os.makedirs(Backup)

    global imagen
    imagen = cv2.imread(Folderpath + '/frame.bmp')

    rangoBajo_b = np.array([0, 0, 250], np.uint8) #Blanco
    rangoAlto_b = np.array([0, 0, 255], np.uint8)

    imagenHSV = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(imagenHSV, rangoBajo_b, rangoAlto_b)

    cnt,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    drawCnt(cnt, (0,255,0))
    
    

    totalLEDs = len(cnt)
    print(totalLEDs)

    cv2.imshow('imagen', imagen)
    cv2.imshow('mask', mask)
    cv2.imwrite(Backup + '/LED_Contour.bmp', imagen)
    cv2.imwrite(Backup + '/mask.bmp', mask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()



pathVerification()
takeFrame()
Inspection()