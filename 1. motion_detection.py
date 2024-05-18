import cv2
import numpy as np
import time
import actions
from dotenv import load_dotenv
import os
import json

load_dotenv()

google_cloud_credentials = os.getenv('GOOGLE_CLOUD_CREDENTIALS')
google_cloud_credentials = json.loads(os.getenv('GOOGLE_CLOUD_CREDENTIALS'))



def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    _, frame1 = cap.read()
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

    last_capture_time = time.time()
    capture_interval = 20  # Interval in seconds

    while True:
        time.sleep(0.1)  # Limit frame rate
        _, frame2 = cap.read()
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

        delta_frame = cv2.absdiff(gray1, gray2)
        thresh_frame = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        contours, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue
            motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 3)

        if motion_detected and (time.time() - last_capture_time > capture_interval):
            actions.handle_detection(frame2)
            last_capture_time = time.time()  # Update the last capture time

        gray1 = gray2.copy()
        cv2.imshow("Motion Detection", frame2)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
