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
        return True
        if not self.cap.isOpened(): return False
    def reset(self):
        # After the loop release the cap object
        self.cap.release()
        # Destroy all the windows
        cv2.destroyAllWindows()

def save_frames(frames):
        folder = dt.now().strftime("%d_%m_%Y")
        path_folder = os.path.join(THIS_FOLDER, f'data/{folder}')
        #print(frames)
        print(frames.shape)

        if not os.path.exists("data/"+folder):
            os.makedirs(f"data/{folder}")
        n = 0
        for time_, frame in zip(times, frames):
            n+=1
            print(frame.shape, n)
            path = path_folder + f"/{time_}_{n}.jpg"
            cv2.imwrite(path,frame)

        print("Saved " + f"{len(frames_buffer)}" + " frames")

def main():
    cam = Camera()
    if not cam.compile():
        print("Camera in use. Try again later.")
        return
    
    clf = cv2.CascadeClassifier('face_detector.xml')
    #clf = cv2.CascadeClassifier('upperbody_detector.xml')
    is_shutdown = False
    itr = 0
    save_interval = 20
    WAIT = 1
    frames_buffer=np.empty(save_interval, dtype=object).flatten()
    times=np.empty(save_interval,dtype=object).flatten()
    while(True):
          
        # Capture the video frame # by frame
        ret, frame = cam.cap.read()
    
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
            frames_buffer[itr-1] = frame
            times[itr] = dt.now().strftime("%H_%M_%S")
            itr += 1
    
        if itr % save_interval == 0 and itr != 0: 
            save_frames(frames=frames_buffer)
            itr = 0
        #else: cv2.destroyAllWindows()
          
        # the 'q' button is set as the quit
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cam.reset()
            save_frames(frames=frames_buffer)
            print("Saved")
            break
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            cam.reset()
            break
    
        time.sleep(3)

if __name__=="__main__":
    main()
