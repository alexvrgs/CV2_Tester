import cv2

cap = cv2.VideoCapture(1)

while cap.isOpened():

    ref, frame = cap.read()

    if ref is not True: break

    cv2.imshow('Frame', frame)


cap.release()
cv2.destroyAllWindow()