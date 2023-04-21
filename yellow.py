import cv2
import numpy as np

cap= cv2.VideoCapture(0)

while(1):

    _, imageFrame = cap.read()

    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    yellow_lower = np.array([22,60,200],np.uint8)
    yellow_upper = np.array([60,255,255],np.uint8)
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)


    kernal = np.ones((5, 5), "uint8")

    yellow_mask = cv2.dilate(yellow_mask, kernal)
    res_yellow = cv2.bitwise_and(imageFrame, imageFrame, mask = yellow_mask)



    contours, hierarchy = cv2.findContours (yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x,y), (x + w, y + h), (40, 100, 120), 2)
            
            center = ((x + w)//2, (y + h)//2)

            cv2.putText(imageFrame, "Yellow Colour"+ str(center), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (40, 100, 120), 2)


    cv2.imshow("Yellow Detection in Real- Time", imageFrame)

    if cv2.waitKey(10) & 0xFF == ord ('q'):
        cap.relase()
        cv2.destroyAllWindows()
        break

cv2.destroyAllWindows()    


   
