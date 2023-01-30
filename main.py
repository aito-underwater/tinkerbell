#!/usr/bin/env python3

'''
always getting the most recent frame of a camera
================================================
Usage:
------
    freshest_camera_frame.py
Keys:
-----
    ESC   - exit
'''

# Python 2/3 compatibility
from __future__ import print_function

import os
import sys
import time
import threading
import numpy as np
import cv2


# also acts (partly) like a cv.VideoCapture
class FreshestFrame(threading.Thread):
    def __init__(self, capture, name='FreshestFrame'):
        self.capture = capture
        assert self.capture.isOpened()

        # this lets the read() method block until there's a new frame
        self.cond = threading.Condition()

        # this allows us to stop the thread gracefully
        self.running = False

        # keeping the newest frame around
        self.frame = None

        # passing a sequence number allows read() to NOT block
        # if the currently available one is exactly the one you ask for
        self.latestnum = 0

        # this is just for demo purposes
        self.callback = None

        super().__init__(name=name)
        self.start()

    def start(self):
        self.running = True
        super().start()

    def release(self, timeout=None):
        self.running = False
        self.join(timeout=timeout)
        self.capture.release()

    def run(self):
        counter = 0
        while self.running:
            # block for fresh frame
            (rv, img) = self.capture.read()
            assert rv
            counter += 1

            # publish the frame
            with self.cond:  # lock the condition for this operation
                self.frame = img if rv else None
                self.latestnum = counter
                self.cond.notify_all()

            if self.callback:
                self.callback(img)

    def read(self, wait=True, seqnumber=None, timeout=None):
        # with no arguments (wait=True), it always blocks for a fresh frame
        # with wait=False it returns the current frame immediately (polling)
        # with a seqnumber, it blocks until that frame is available (or no wait at all)
        # with timeout argument, may return an earlier frame;
        #   may even be (0,None) if nothing received yet

        with self.cond:
            if wait:
                if seqnumber is None:
                    seqnumber = self.latestnum + 1
                if seqnumber < 1:
                    seqnumber = 1

                rv = self.cond.wait_for(lambda: self.latestnum >= seqnumber, timeout=timeout)
                if not rv:
                    return (self.latestnum, self.frame)

            return (self.latestnum, self.frame)


def main():
    # these windows belong to the main thread
    cv2.namedWindow("frame")
    # on win32, imshow from another thread to this DOES work
    cv2.namedWindow("realtime")

    # open some camera
    cap = cv2.VideoCapture('rtsp://admin:123456@192.168.1.237/H264?ch=1&subtype=0')
    cap.set(cv2.CAP_PROP_FPS, 60)

    # wrap it
    fresh = FreshestFrame(cap)

    # a way to watch the camera unthrottled
    def callback(img):
        pass

    # main thread owns windows, does waitkey

    fresh.callback = callback

    # main loop
    # get freshest frame, but never the same one twice (cnt increases)
    # see read() for details
    cnt = 0
    while True:
        # test that this really takes NO time
        # (if it does, the camera is actually slower than this loop and we have to wait!)
        t0 = time.perf_counter()
        ret, frame = fresh.read(seqnumber=cnt + 1)
        dt = time.perf_counter() - t0
        if dt > 0.010:  # 10 milliseconds
            print("NOTICE: read() took {dt:.3f} secs".format(dt=dt))

        # let's pretend we need some time to process this frame
        print("processing {cnt}...".format(cnt=cnt), end=" ", flush=True)


        # -----------------------------------------------------------

       # ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # red
        lower_red = np.array([136, 87, 111])
        upper_red = np.array([180, 255, 255])
        red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
        frame = cv2.bitwise_and(frame, frame, mask=red_mask)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blurred = cv2.blur(gray, (3, 3))
        detected_circles = cv2.HoughCircles(gray_blurred,
                                            cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                            param2=30, minRadius=1, maxRadius=40)

        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))

            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]

                cv2.circle(frame, (a, b), r, (0, 255, 0), 2)
                cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)

                print(a, b)

        cv2.imshow("Red", frame)
        key = cv2.waitKey(200)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# ----------------------------------------------------------------
        # this keeps both imshow windows updated during the wait (in particular the "realtime" one)



        print("done!")

    fresh.release()

    cv2.destroyWindow("frame")
    cv2.destroyWindow("realtime")


if __name__ == '__main__':
    main()
