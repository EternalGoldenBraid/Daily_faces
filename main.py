import cv2
import numpy as np
import matplotlib.pyplot as plt

import time
from datetime import datetime as dt
import os
import signal

# define a video capture object
WAIT = 1
  
buffer=0
frames=[]

class Camera():
    def __init__(self):
        self.vid = None;
    def compile(self):
        self.vid = cv2.VideoCapture(0)
    def reset(self):
        # After the loop release the cap object
        self.vid.release()
        # Destroy all the windows
        cv2.destroyAllWindows()

cam = Camera()
cam.compile()

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

clf = cv2.CascadeClassifier('face_detector.xml')
#clf = cv2.CascadeClassifier('upperbody_detector.xml')
times = []
is_shutdown = False
while(True):
      
    # Capture the video frame # by frame
    ret, frame = cam.vid.read()

    faces_rects = clf.detectMultiScale(frame, scaleFactor = 1.2, minNeighbors = 5);
    
    #for (x,y,w,h) in faces_rects:
    if not len(faces_rects) == 0:
        for x,y,w,h in faces_rects:
            #x,y,w,h = rect
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #frame = frame[y:y+h, x:x+w]

    # Display the resulting frame
    if len(faces_rects) != 0:
        cv2.imshow('frame', frame)
        frames.append(frame)
        times.append(dt.now().strftime("%H_%M_%S"))
    #else: cv2.destroyAllWindows()
      
    # the 'q' button is set as the quit
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cam.reset()
        folder = dt.now().strftime("%d_%m_%Y")
        #name = dt.now().strftime("%H_%M_%S")
        path_folder = os.path.join(THIS_FOLDER, f'data/{folder}')

        if not os.path.exists("data/"+folder):
            os.makedirs(f"data/{folder}")
        n = 0
        print("FRAMES: ", len(frames))
        for time_, frame in zip(times, frames):
            n+=1
            path = path_folder + f"/{time_}_{n}.jpg"
            cv2.imwrite(path,frame)
        print("Saved")
        break
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        cam.reset()
        break

    #time.sleep(WAIT)

