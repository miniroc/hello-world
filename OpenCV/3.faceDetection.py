import cv2
import numpy as np
import matplotlib.pyplot as plt

#0 is default camera
cap = cv2.VideoCapture(0)

while(1):	
#	take each frame, return tuple
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	face_cascade = cv2.CascadeClassifier('C:\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_default.xml')
	eye_cascade = cv2.CascadeClassifier('C:\\opencv\\sources\\data\\haarcascades\\haarcascade_eye.xml')
	
#The detected objects are returned as a list of rectangles
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
		eyes = eye_cascade.detectMultiScale(roi_gray)
		for (ex,ey,ew,eh) in eyes:
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

		cv2.imshow('img',frame)
				
		k = cv2.waitKey(5) & 0xFF
#escape key to exit
	if k==27:
#	print hsvImg[390,370]
		break

cap.release()
cv2.destroyAllWindows()


