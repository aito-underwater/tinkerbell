import cv2
import cv2 as cv
import numpy as np

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    

    # yellow
    yellow_lower = np.array([22,60,200],np.uint8)
    yellow_upper = np.array([60,255,255],np.uint8)
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)
    frame = cv2.bitwise_and(frame, frame, mask = yellow_mask)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3))

    
    cv2.imshow("Yellow", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()
