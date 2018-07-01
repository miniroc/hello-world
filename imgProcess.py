import cv2
import numpy as np
import matplotlib

def main():
    print(cv2.__version__)
    cv2.namedWindow("Try Filter", cv2.WINDOW_AUTOSIZE)
    src = cv2.imread("d:\\cv2Img.jpg",cv2.IMREAD_COLOR)
    
    if src is None:
        print("failed to read image!")
        return -1
    
    cv2.imshow("original img", src)

#     blurImg = cv2.blur(src, (3, 3))
    GaussianBlurImg = cv2.GaussianBlur(src, (5, 5),2)
#     MedianBlurImg = cv2.medianBlur(src,3)    
#      cv2.imshow("Box FIlter", blurImg)
#     cv2.imshow("Gaussian Blur", GaussianBlurImg)
#     cv2.imshow("Median Blur", MedianBlurImg)

#     srcgray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
#     cv2.imshow(srcgray)
    
#   Usage: dst = cv.Sobel(src, ddepth, dx, dy[, ksize[, scale[, delta[, borderType]]]])
    sobel_x = cv2.Sobel(GaussianBlurImg, cv2.CV_16S, 1, 0, 5)
    sobel_y = cv2.Sobel(GaussianBlurImg, cv2.CV_16S, 0, 1, 5)
    sobelEdge = cv2.addWeighted(cv2.convertScaleAbs(sobel_x), 0.5, cv2.convertScaleAbs(sobel_y), 0.5, 0)
    cv2.imshow("Sobel edge detector", sobelEdge)
    
#   usage: edges = cv.Canny(image, threshold1, threshold2[, apertureSize[, L2gradient]])
    cannyEdge = cv2.Canny(GaussianBlurImg, 80, 80*3, 5)
    cv2.imshow("Canny Edge Detector", cannyEdge)
    
    c = cv2.waitKey()
    
    
if __name__ == "__main__":
    main()