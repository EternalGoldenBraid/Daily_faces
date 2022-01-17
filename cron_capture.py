import cv2
import numpy as np
import matplotlib.pyplot as plt

import time
from datetime import datetime as dt
import os
import signal

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# define a video capture object
class Camera():
    def __init__(self):
        self.cap = None;
    def compile(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return False
        return True
    def reset(self):
        # After the loop release the cap object
        self.cap.release()
        # Destroy all the windows
        cv2.destroyAllWindows()

def save_frames(frame, name):
        folder = dt.now().strftime("%d_%m_%Y")
        path_folder = os.path.join(THIS_FOLDER, f'data/{folder}')

        if not os.path.exists("data/"+folder):
            os.makedirs(f"data/{folder}")
        path = path_folder + f"/{name}.jpg"
        cv2.imwrite(path,frame)

def cron_cap():
    cam = Camera()
    if not cam.compile():
        print("Camera in use. Try again later.")
        return
    print("Compiled")
    
    clf = cv2.CascadeClassifier('face_detector.xml')
    #clf = cv2.CascadeClassifier('upperbody_detector.xml')
    is_shutdown = False

    # Capture the video frame # by frame and detect face.
    ret, frame = cam.cap.read()
    # TODO: GRAYSCALE
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.equalizeHist(frame)
    print(frame.shape)
    #if ret :faces_rects = clf.detectMultiScale(frame, scaleFactor = 1.2, minNeighbors = 0);
    if ret :faces_rects = clf.detectMultiScale(frame);
    else:
        print("Image capture unsuccesful.")
        return
    print("Image captured.")
    
    # Save if face
    if not len(faces_rects) == 0:
        print("Face detected, saving...")
        for x,y,w,h in faces_rects:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        frame = frame[y:y+h, x:x+w]
    else: print("No face detected.")
    
    # Display the resulting frame
    if len(faces_rects) != 0:
        cv2.imshow('frame', frame)
        name = dt.now().strftime("%H_%M_%S")
        save_frames(frame, name)

    cam.reset()

cron_cap()
