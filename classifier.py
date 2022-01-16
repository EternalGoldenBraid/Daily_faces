import numpy as np
import cv2
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

#Converting to grayscale
#img = cv2.imread('data/training_2.png')
#img = cv2.imread('data/face.jpg')
img = cv2.imread('data/test_3.jpg',3)
#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow("image",img)

plt.imshow(img)
plt.show()


clf = cv2.CascadeClassifier('face_detector.xml')
faces_rects = clf.detectMultiScale(img, scaleFactor = 1.2, minNeighbors = 5);

for (x,y,w,h) in faces_rects:
         cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

plt.imshow(img)
plt.show()
