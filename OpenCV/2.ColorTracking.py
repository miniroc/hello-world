import cv2
#import highgui as hg
import numpy as np
import matplotlib.pyplot as plt

def nothing(x):
	pass


# Create Windows
cv2.namedWindow("HSV threshold",cv2.WINDOW_NORMAL)
#create Trackbar: trackbar name, window name, min, max, recall function
cv2.createTrackbar("Hmin", "HSV threshold", 0, 255, nothing);
cv2.createTrackbar("Hmax", "HSV threshold", 0, 255, nothing);
cv2.createTrackbar("Smin", "HSV threshold", 0, 255, nothing);
cv2.createTrackbar("Smax", "HSV threshold", 0, 255, nothing);
cv2.createTrackbar("Vmin", "HSV threshold", 0, 255, nothing);
cv2.createTrackbar("Vmax", "HSV threshold", 0, 255, nothing);

Hmax=cv2.setTrackbarPos('Hmax','HSV threshold',255)
Smax=cv2.setTrackbarPos('Smax','HSV threshold',255)
Vmax=cv2.setTrackbarPos('Vmax','HSV threshold',255)

#0 is default camera
cap = cv2.VideoCapture(0)

while(1):	
#	take each frame, return tuple
	ret, frame = cap.read()
	
#convert BGR to HSV
	hsvImg = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#get adjusted min,max value
	Hmin=cv2.getTrackbarPos('Hmin','HSV threshold')
	Smin=cv2.getTrackbarPos('Smin','HSV threshold')
	Vmin=cv2.getTrackbarPos('Vmin','HSV threshold')
	Hmax=cv2.getTrackbarPos('Hmax','HSV threshold')
	Smax=cv2.getTrackbarPos('Smax','HSV threshold')
	Vmax=cv2.getTrackbarPos('Vmax','HSV threshold')
#lower and upper color bundary
	lower_color = (Hmin,Smin,Vmin)
	upper_color = (Hmax,Smax,Vmax)
#filter with lower color and max color
	mask = cv2.inRange(hsvImg, lower_color, upper_color)
	
#bitwise-and mask
	andResultImg = cv2.bitwise_and(frame, frame, mask=mask)

#morphology opening: erosion followed by dialation
	kernel = np.ones((5,5),np.uint8)
	openingResultImg = cv2.morphologyEx(andResultImg, cv2.MORPH_OPEN, kernel)
	
#findContour() for further operation
	grayImg = cv2.cvtColor(openingResultImg, cv2.COLOR_BGR2GRAY)
	retval,threImg = cv2.threshold(grayImg, 20, 255 , cv2.THRESH_BINARY)
	_,contours,hierarchy = cv2.findContours(threImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#cv2.moments(contours) for more information. centroid cx=int(M['m01']/M['m00']),cy=int(M['m01']/M['m00'])

#mark object
	for cnt in contours:
		rect=cv2.minAreaRect(cnt)
		box=cv2.boxPoints(rect)
		box=np.int0(box)
		cv2.drawContours(frame,[box],0,(0,0,255),2)


	cv2.imshow('frame',frame)
#	cv2.imshow('mask',mask)
#	cv2.imshow('andResultImg',andResultImg)
	cv2.imshow('openingResultImg',openingResultImg)
	
	k = cv2.waitKey(5) & 0xFF
	#escape key to exit
	if k==27:
#		print hsvImg[390,370]
		break

cap.release()
cv2.destroyAllWindows()