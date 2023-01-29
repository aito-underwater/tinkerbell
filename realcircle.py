import cv2
import cv2 as cv
import numpy as np

cap = cv2.VideoCapture(0)

while (1):
    
    _, imageFrame = cap.read()
    
    gray = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3))
    detected_circles = cv2.HoughCircles(gray_blurred, 
                       cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                   param2 = 30, minRadius = 1, maxRadius = 40)
  

    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
  
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
  
            cv2.circle(imageFrame, (a, b), r, (0, 255, 0), 2)
            cv2.circle(imageFrame, (a, b), 1, (0, 0, 255), 3)

s
        cv.imshow('Detected Circle', imageFrame)
    
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        cap.relase()
        cv2.destroyAllWindows()
        break

cv2.destroyAllWindows()   


