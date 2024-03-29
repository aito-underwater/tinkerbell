import cv2
import numpy as np

cap = cv2.VideoCapture('rtsp://admin:123456@192.168.1.237/H264?ch=1&subtype=0')

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        if radius > 10:
            cv2.circle(frame, center, radius, (0, 0, 255), 2)
            cv2.circle(frame, center, 3, (0, 255, 0), -1)
            cv2.putText(frame, "({}, {})".format(center[0], center[1]), (center[0] + 10, center[1] + 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            if len(contour) >= 5:
                ellipse = cv2.fitEllipse(contour)
                cv2.ellipse(frame, ellipse, (0, 0, 255), 2)
                center = ellipse[0]
                cv2.circle(frame, (int(center[0]), int(center[1])), 3, (0, 255, 0), -1)
                cv2.putText(frame, "({}, {})".format(int(center[0]), int(center[1])),
                            (int(center[0]) + 10, int(center[1]) + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
