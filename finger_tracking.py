import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def train_hsv(path):
    images = os.listdir(path)
    H = []
    S = []
    c=0
    for img_name in images:
        print(c)
        c+=1
        img_path=os.path.join(path, img_name)
        img = cv2.imread(img_path)
        I = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        for i in range(I.shape[0]):
            for j in range(I.shape[1]):
                if(I[i][j][1]>35):
                    H.append(I[i][j][0])
                    S.append(I[i][j][1])
    hist, x, y = np.histogram2d(H, S, bins=[np.arange(257),np.arange(257)])
    norm = hist/hist.max()
    plt.imshow(norm)
    plt.colorbar()
    plt.show()
    np.save("histogram_small.npy", norm)
    return norm

def skin_segmentation(img, hist, thresh):
    I = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    (ht, w, d) = I.shape
    L = np.zeros((ht,w,d))
    for i in range(ht):
        for j in range(w):
            hue=I[i][j][0]
            sat=I[i][j][1]
            #histogram works like a look up table here
            if(hist[hue][sat]>thresh):
                L[i][j][0]=img[i][j][0]
                L[i][j][1]=img[i][j][1]
                L[i][j][2]=img[i][j][2]
            else:
                L[i][j][0]=0
                L[i][j][1]=0
                L[i][j][2]=0
    return L

def main():
    path = '/home/ritz/SpringQ/CV/CVgame/assests/Hands_small'
    # hist_hsv=train_hsv(path)
    # print("Hist Created")
    hist_hsv=np.load("histogram_small.npy")
    cap = cv2.VideoCapture(0)
    width, height = 1280, 720
    cap.set(3, width)
    cap.set(4, height)

    thresh_HSV=0.028
    while True:
        ret, frame = cap.read()
        # frame = cv2.flip(frame, 1)
        frame = cv2.bilateralFilter(frame, 5, 50, 100)  # Smoothing
        frame = cv2.flip(frame, 1)  #Horizontal Flip
        # img=skin_segmentation(frame, hist_hsv, thresh_HSV)
        # cv2.imshow('original', img)
        #MAYBE DO GAUSSIAN BLUR
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        objectSegment = cv2.calcBackProject([hsv], [0,1], hist_hsv, [0,180,0,256], 1)
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
        cv2.filter2D(objectSegment, -1, disc, objectSegment)
        _, threshObjectSegment = cv2.threshold(objectSegment,70,255,cv2.THRESH_BINARY)

        threshObjectSegment = cv2.merge((threshObjectSegment,threshObjectSegment,threshObjectSegment))
        locatedObject = cv2.bitwise_and(frame, threshObjectSegment)

        locatedObjectGray = cv2.cvtColor(locatedObject, cv2.COLOR_BGR2GRAY)
        _, locatedObjectThresh = cv2.threshold(locatedObjectGray, 70, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        locatedObject = cv2.medianBlur(locatedObjectThresh, 5)
        cv2.imshow('original', locatedObject)
        # dst = cv2.calcBackProject([hsv], [0, 1], hist_hsv, [0, 180, 0, 256], 1)
        # dst = skin_segmentation()
        # disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
        # cv2.filter2D(dst, -1, disc, dst)
        # ret, thresh = cv2.threshold(dst, 150, 255, cv2.THRESH_BINARY)
        # thresh = cv2.merge((thresh, thresh, thresh))
        # skinMask = cv2.bitwise_and(frame, thresh)
        # cv2.imshow('original', img)
        k= cv2.waitKey(10)
        if k==27:
            break
    cv2.destroyAllWindows()

if __name__ == '__main__': 
    main()