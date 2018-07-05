import numpy as np
import cv2  
import time    
from Tkinter import *

def hasObject(frame1,frame2):
#	change from BGR 2 GRAY
	frame11 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
	frame22 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

#difference of the following 2 frames
	diffframe = cv2.absdiff(frame11, frame22)
	cv2.namedWindow('diff', cv2.WINDOW_NORMAL)
	cv2.imshow('diff',diffframe)

#find contour
	ret,thresh = cv2.threshold(diffframe,100,255,cv2.THRESH_BINARY)
	cv2.namedWindow('thresh',cv2.WINDOW_NORMAL)
	cv2.imshow('thresh',thresh)
#	return True
#	contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # !!!!!three parameters returned!!!!!
#	print len(contours)
	if len(contours) > 0:
#		print "return True"
		return True
	else:
#		print "return False"
		return False





#videoCap is a VideoCapture class object
videoCap = cv2.VideoCapture(0) 

#filename string
filename = "E:\\OpenCV-Python\\recordVideo.avi"
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#access some of the features of this video using cap.get(propId) method where propId is a number from 0 to 18
#You scan check the frame width and height by cap.get(3) and cap.get(4)
#width = videoCap.get(3)	#return float type
#height = videoCap.get(4)
#print width
#print height
#videoWriter = cv2.VideoWriter(filename, fourcc, 20.0, (640,480))
#get frame rate, works for stored video, don't work for real time capture
#fps = videoCap.get(cv2.CAP_PROP_FPS)
#print fps
ret, fframe = videoCap.read()
#(width,height,depth) = fframe.shape
(width,height) = fframe.shape[:2]
videoWriter = cv2.VideoWriter(filename, fourcc, 10.0, (height,width))

while(videoCap.isOpened()):
#	Capture frame-by-frame
#	ret, frame = videoCap.read()
#	
#	Our operations on the frame come here
#	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#	Display the resulting frame
#	cv2.imshow('frame',gray)     
	   
	ret, frame1 = videoCap.read()
     
	if ret==True:
		ret, frame2 = videoCap.read()
		
#		check if moving objects in the frame
		detectedObj = hasObject(frame1,frame2)
		
#		write video
		if detectedObj == True:
			#The function time.time() returns the current system time in ticks since 12:00am, January 1, 1970(epoch).
			stamp = time.asctime(time.localtime(time.time()))
			cv2.putText(frame1,stamp,(0,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,255)
			
#			print "write frame"
			videoWriter.write(frame1)

		cv2.imshow('frame',frame1)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		break

# Release everything if job is finished
videoCap.release()
videoWriter.release()
cv2.destroyAllWindows()