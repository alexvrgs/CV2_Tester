import cv2
import numpy as np
import os

#--> Functions <----------------------------------------------------------------------------------------------------------

def dibujar_cnt (mask, color):
    global f_OK
    cnt,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnt:
        area = cv2.contourArea(c)
        if area > 10:
            x, y, w, h = cv2.boundingRect(c)
            if color == (0, 255, 0):
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                f_OK = auxFrame[y:y+h, x:x+w]
                f_OK = cv2.resize(f_OK, (150, 150), interpolation = cv2.INTER_CUBIC)
                cv2.putText(frame, 'OK', (x+20, y+10), font, 0.5, color, 2, cv2.LINE_AA)

                if k == ord('s'):
                    cv2.imwrite('Imagenes/frame_{}.png'.format(count), f_OK)
                    cv2.imshow('Img', f_OK) 

            if color == (0, 0, 255):
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.line(frame, (x, y), (x+w, y+h), color, 3)
                cv2.putText(frame, 'NOK', (x+20, y+10), font, 0.5, color, 2, cv2.LINE_AA)
            
            # nuevoContorno = cv2.convexHull(c)
            # cv2.drawContours(gray, [nuevoContorno], 0, color, 2)
            # cv2.drawContours(frame, [nuevoContorno], 0, color, 2)

def createFolder():
    if not os.path.exists('Imagenes'):
        print("Carpeta creada: Imagenes")
        os.makedirs('Imagenes')

#--> Main Script <--------------------------------------------------------------------------------------------------------
createFolder()

video = cv2.VideoCapture(1, cv2.CAP_DSHOW)

rangoBajo_b = np.array([0, 0, 250], np.uint8) #Blanco
rangoAlto_b = np.array([0, 0, 255], np.uint8)

rangoBajo = np.array([0, 0, 120], np.uint8) #Gris
rangoAlto = np.array([0, 0, 170], np.uint8)

# rangoBajo = np.array([100, 100, 20], np.uint8) #Azul
# rangoAlto = np.array([125, 255, 255], np.uint8)

font = cv2.FONT_HERSHEY_SIMPLEX

count = 0

while video.isOpened():
    ret, frame = video.read()
    if ret is not True: break

    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask_NOK = cv2.inRange(frameHSV, rangoBajo, rangoAlto)
    mask_OK = cv2.inRange(frameHSV, rangoBajo_b, rangoAlto_b)

    auxFrame = frame.copy()
    
    k = cv2.waitKey(1)
    if k == 27: break

    dibujar_cnt(mask_OK, (0,255,0))
    dibujar_cnt(mask_NOK, (0,0,255))

    # cv2.imshow('mask', mask)
    cv2.imshow('Video', frame)
    # cv2.imshow('Gray', gray)

    

video.release()
cv2.destroyAllWindows()