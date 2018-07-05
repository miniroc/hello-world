import cv2
import numpy as np

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

cv2.createTrackbar("fingerMinAngle", "HSV threshold", 0, 180, nothing);
cv2.createTrackbar("fingerMaxAngle", "HSV threshold", 0, 180, nothing);
cv2.createTrackbar("fingerBoundRatio", "HSV threshold", 1, 100, nothing);
cv2.createTrackbar("fingerCenterMinAngle", "HSV threshold", 0, 180, nothing);
cv2.createTrackbar("fingerCenterMaxAngle", "HSV threshold", 0, 180, nothing);

Hmax=cv2.setTrackbarPos('Hmin','HSV threshold',0)
Hmax=cv2.setTrackbarPos('Hmax','HSV threshold',196)
Smax=cv2.setTrackbarPos('Smin','HSV threshold',38)
Smax=cv2.setTrackbarPos('Smax','HSV threshold',168)
Vmax=cv2.setTrackbarPos('Vmin','HSV threshold',40)
Vmax=cv2.setTrackbarPos('Vmax','HSV threshold',210)

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
	
#	median filter
	median=cv2.medianBlur(andResultImg,5)

#morphology opening: erosion followed by dialation
	kernel = np.ones((8,8),np.uint8)
#	openingResultImg = cv2.morphologyEx(andResultImg, cv2.MORPH_OPEN, kernel)
	openingResultImg = cv2.dilate(andResultImg, kernel)
	
#findContour() for further operation
	grayImg = cv2.cvtColor(openingResultImg, cv2.COLOR_BGR2GRAY)
######### threshImg is the key image, adjust threshold #########
	retval,threImg = cv2.threshold(grayImg, 20, 255 , cv2.THRESH_BINARY) 
	cv2.imshow('threImg',threImg)
	_,contours,hierarchy = cv2.findContours(threImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#cv2.moments(contours) for more information. centroid cx=int(M['m01']/M['m00']),cy=int(M['m01']/M['m00'])

##mark object
#	for cnt in contours:
#		rect=cv2.minAreaRect(cnt)
#		box=cv2.boxPoints(rect)
#		box=np.int0(box)
#		cv2.drawContours(frame,[box],0,(0,0,255),2)

#find biggest contours
	if len(contours)>0:
		largestCntIndex=0
		largestArea= cv2.contourArea(contours[0])
		 
		i = 0	
		while i < len(contours):
			area = cv2.contourArea(contours[i])
			if  area > largestArea:
				largestCntIndex=i
				largestArea = area
			i+=1
#		print len(contours)	
#		print largestCntIndex
#		print largestArea
		
		largestCnt=contours[largestCntIndex]
#		cv2.drawContours(frame, contours[0], 0, (0,255,0), 3)
#		cv2.drawContours(frame, [contours[largestCntIndex]], 0, (0,255,0), 5) ###############have to use [contours[largestCntIndex]], if use contours[largestCntIndex],will only draw a point
		cv2.drawContours(frame, contours[largestCntIndex], -1, (255,0,0), 2)  ############### use -1 indicates draw all
#		cv2.drawContours(frame, largestCnt, 0, (0,0,255), 1)
#		cv2.imshow('frame',frame)
#		cv2.imshow('mask',mask)
		cv2.imshow('andResultImg',andResultImg)
		cv2.imshow('openingResultImg',openingResultImg)


######### find finger tips #########
		hull = cv2.convexHull(largestCnt,returnPoints=False)
		defects = cv2.convexityDefects(largestCnt,hull)
		
		boundx,boundy,boundw,boundh = cv2.boundingRect(largestCnt)
		cv2.rectangle(frame,(boundx,boundy),(boundx+boundw,boundy+boundh),(255,0,0),2)
		boundcenterx=boundx+boundw/2
		boundcentery=boundy+boundh/2
		
		fingerMinAngle=cv2.getTrackbarPos("fingerMinAngle", "HSV threshold")
		fingerMaxAngle=cv2.getTrackbarPos("fingerMaxAngle", "HSV threshold")
		fingerCenterMinAngle=cv2.getTrackbarPos("fingerCenterMinAngle", "HSV threshold")
		fingerCenterMaxAngle=cv2.getTrackbarPos("fingerCenterMaxAngle", "HSV threshold")

		
		for i in range(defects.shape[0]):
			s,e,f,d = defects[i,0]
			start = tuple(largestCnt[s][0])
			end = tuple(largestCnt[e][0])
			far = tuple(largestCnt[f][0])
#			if it's finger tip
			SE=np.sqrt((start[0]-end[0])*(start[0]-end[0])+(start[1]-end[1])*(start[1]-end[1]))
			SF=np.sqrt((start[0]-far[0])*(start[0]-far[0])+(start[1]-far[1])*(start[1]-far[1]))
			EF=np.sqrt((end[0]-far[0])*(end[0]-far[0])+(end[1]-far[1])*(end[1]-far[1]))
#			Law of cosines: c*c = a*a + b*b - 2abcos(alpha)
			angle=np.arccos((SF*SF+EF*EF-SE*SE)/(2*SF*EF))
			degree=np.degrees(angle)
#			use angle to filter unwanted defect points
			if degree > fingerMinAngle and degree < fingerMaxAngle:
#			use distance to filter out unwanted defect points
				if SF > (0.3*boundh) and SF <boundh:
					SC=np.sqrt((start[0]-boundcenterx)*(start[0]-boundcenterx)+(start[1]-boundcentery)*(start[1]-boundcentery))
					EC=np.sqrt((end[0]-boundcenterx)*(end[0]-boundcenterx)+(end[1]-boundcentery)*(end[1]-boundcentery))
					angle=np.arccos((SF*SF+EF*EF-SE*SE)/(2*SF*EF))
#					Law of cosines: c*c = a*a + b*b - 2abcos(alpha)
					angle2=np.arccos((SC*SC+EC*EC-SE*SE)/(2*SC*EC))
					degree2=np.degrees(angle2)
					if degree2 > fingerCenterMinAngle and degree2 < fingerCenterMaxAngle:		
						cv2.line(frame,start,far,[0,255,0],2)
						cv2.line(frame,end,far,[0,255,0],2)
						cv2.circle(frame,start,5,[0,0,255],-1)
						cv2.circle(frame,end,5,[0,0,255],-1)
		cv2.imshow('frame',frame)
		
		
    
	k = cv2.waitKey(5) & 0xFF
	#escape key to exit
	if k==27:
#		print hsvImg[390,370]
		break

cap.release()
cv2.destroyAllWindows()