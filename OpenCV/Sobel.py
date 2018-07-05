import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('E:\\OpenCV-Python\\captureRed.jpg', 0)

cv2.imshow('img', img)

laplacian32f = cv2.Laplacian(img, cv2.CV_32F)
sobelx32f = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=5)
sobely32f = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=5)

absLapacian32f = np.absolute(laplacian32f)
absSobelx32f = np.absolute(sobelx32f)
absSobely32f = np.absolute(sobely32f)

# laplacian = np.unit8(absLapacian32f)
# sobelx = np.unit8(absSobelx32f)
# sobely = np.unit8(absSobely32f) 

cv2.imshow('Laplacian', absLapacian32f)
cv2.imshow('Sobelx', absSobelx32f)
cv2.imshow('sobely', absSobely32f)

plt.subplot(2,2,1)
plt.imshow(laplacian32f, cmap='gray')

cv2.waitKey(0)
cv2.destroyAllWindows()



