import cv2
import numpy as np

# Load the IP camera stream
cap = cv2.VideoCapture('rtsp://admin:123456@192.168.1.237/H264?ch=1&subtype=0')

while True:
    # Capture a frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use the HoughCircles function to detect circles in the image
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

    # If circles are detected
    if circles is not None:
        # Convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # Loop over the circles
        for (x, y, r) in circles:
            # Draw the circle in the output image
            cv2.circle(frame, (x, y), r, (0, 0, 255), 2)

            # Print the coordinates of the center of the circle
            print("Circle center: ({}, {})".format(x, y))

    # Use the HoughCircles function to detect ellipses in the image
    ellipses = cv2.fitEllipse(circles)

    # If ellipses are detected
    if ellipses is not None:
        # Draw the ellipse in the output image
        cv2.ellipse(frame, ellipses, (0, 0, 255), 2)

        # Print the coordinates of the center of the ellipse
        print("Ellipse center: ({}, {})".format(ellipses[0][0], ellipses[0][1]))

    # Display the resulting frame
    cv2.imshow("Frame", frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()

# Close all the windows
cv2.destroyAllWindows()
