import cv2
import cv2 as cv
import numpy as np

cap = cv2.VideoCapture('rtsp://admin:123456@192.168.1.237/80')


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    # red
    lower_red = np.array([136, 87, 111])
    upper_red = np.array([180, 255, 255])
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
    frame = cv2.bitwise_and(frame, frame, mask = red_mask)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3))
    detected_circles = cv2.HoughCircles(gray_blurred,
                       cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                   param2 = 30, minRadius = 1, maxRadius = 40)


    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            cv2.circle(frame, (a, b), r, (0, 255, 0), 2)
            cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)

            print (a,b)



    cv2.imshow("Red", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
