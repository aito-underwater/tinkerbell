import cv2
import numpy as np
import serial
import struct
import time

print("start")

ser = serial.Serial('/dev/ttymxc0', 115200, timeout=None) # replace ttyS1 with the appropriate serial port
message = ''

cap = cv2.VideoCapture('rtsp://admin:123456@192.168.1.237/H264?ch=1-s1?tcp&subtype=0')


def send_data(a,b):
    #package = b''

    #for i in cor:
    package = struct.pack('ii', a, b)
    print(package)

    # Sent string value,but if tests shows us it is wrong turn it on btye
    ser.write(package)

    # Do nothing for 500 milliseconds (0.5 seconds)
    #time.sleep(0.5)


while True:

    if not cap.isOpened():
        print("Kameradan görüntü alınamadı. 3 saniye bekleyin ve tekrar deneyin...")
        time.sleep(3)
        continue

    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)

        _ , contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = str((int(x), int(y))).encode('utf-8')
            radius = int(radius)
            if radius > 10:
              #  cv2.circle(frame, center, radius, (0, 0, 255), 2)
              #  v2.circle(frame, center, 3, (0, 255, 0), -1)
              #  2.putText(frame, "({}, {})".format(center[0], center[1]), (center[0] + 10, center[1] + 10),
              #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                #ser.write(center)
                xx = int(x)
                yy = int(y)
                send_data(xx,yy)

            else:
                if len(contour) >= 5:
                    ellipse = cv2.fitEllipse(contour)
                    cv2.ellipse(frame, ellipse, (0, 0, 255), 2)
                    center = ellipse[0]
                    cv2.circle(frame, (int(center[0]), int(center[1])), 3, (0, 255, 0), -1)
                    cv2.putText(frame, "({}, {})".format(int(center[0]), int(center[1])),
                                (int(center[0]) + 10, int(center[1]) + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        #cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
