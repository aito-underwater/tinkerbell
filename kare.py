import cv2
import numpy as np

cap = cv2.VideoCapture('rtsp://admin:123456@192.168.1.237/H264?ch=1&subtype=0')

min_area = float("inf")
min_contour = None

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue
        approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
            area = cv2.contourArea(contour)
            print("Alan: {} koordinat: ({}, {})".format(area, cX, cY))
            if area < min_area:
                min_area = area
                min_contour = contour
    if min_contour is not None:
        M = cv2.moments(min_contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        print("En küçük alanın koordinatı: ({}, {})".format(cX, cY))
        min_area = float("inf")
        min_contour = None
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
