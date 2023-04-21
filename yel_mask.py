import cv2
import cv2 as cv
import numpy as np

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    

    # yellow
    yellow_lower = np.array([22,60,230],np.uint8)
    yellow_upper = np.array([60,255,255],np.uint8)
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)
    frame = cv2.bitwise_and(frame, frame, mask = yellow_mask)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3))

    contours, hierarchy = cv2.findContours (yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            hsvFrame = cv2.rectangle(hsvFrame, (x,y), (x + w, y + h), (40, 100, 120), 2)
            
            center = ((x + w)//2, (y + h)//2)

            print (hsvFrame, "Yellow Colour"+ str(center), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (40, 100, 120), 2)

    
    cv2.imshow("Yellow", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()
