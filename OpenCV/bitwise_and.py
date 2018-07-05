import numpy as np
import cv2

def findColorRange(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		print 'pixel'
		print watchGray[x,y]


watch = cv2.imread("watch.jpg",cv2.IMREAD_COLOR)
watchGray = cv2.cvtColor(watch, cv2.COLOR_BGR2GRAY)

cv2.namedWindow('gray')
cv2.setMouseCallback('gray', findColorRange)

ret, mask = cv2.threshold(watchGray, 240, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('mask',mask)
mask_inv = cv2.bitwise_not(mask)


img = cv2.imread("capture.jpg",cv2.IMREAD_COLOR)


rows,cols,channels = watch.shape
print rows,cols,channels

ROI = img[0:rows, 0:cols]

img_bg = cv2.bitwise_and(ROI,ROI,mask = mask_inv)
cv2.imshow('img_bg',img_bg)
watch_fg = cv2.bitwise_and(watch,watch,mask = mask)
cv2.imshow('watch_fg',watch_fg)

dst = cv2.add(img_bg, watch_fg)

img[0:rows,0:cols]=dst
cv2.imshow('img',img)

cv2.waitKey(0)
cv2.destroyAllWindows()

#print("hello World")
