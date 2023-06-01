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
    np.save("histogram.npy", norm)
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

# def farthest_point(defects, contour, centroid):
#     if defects is not None and centroid is not None:
#         s = defects[:, 0][:, 0]
#         cx, cy = centroid

#         x = np.array(contour[s][:, 0][:, 0], dtype=np.float64)
#         y = np.array(contour[s][:, 0][:, 1], dtype=np.float64)

#         xp = cv2.pow(cv2.subtract(x, cx), 2)
#         yp = cv2.pow(cv2.subtract(y, cy), 2)
#         dist = cv2.sqrt(cv2.add(xp, yp))

#         dist_max_i = np.argmax(dist)

#         if dist_max_i < len(s):
#             farthest_defect = s[dist_max_i]
#             farthest_point = tuple(contour[farthest_defect][0])
#             return farthest_point
#         else:
#             return None

# def calculateFingers(res, drawing):
#     #  convexity defect
#     hull = cv2.convexHull(res, returnPoints=False)
#     if len(hull) > 3:
#         defects = cv2.convexityDefects(res, hull)
#         if defects is not None:
#             cnt = 0
#             for i in range(defects.shape[0]):  # calculate the angle
#                 s, e, f, d = defects[i][0]
#                 start = tuple(res[s][0])
#                 end = tuple(res[e][0])
#                 far = tuple(res[f][0])
#                 a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
#                 b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
#                 c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
#                 angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
#                 if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
#                     cnt += 1
#                     cv2.circle(drawing, far, 8, [211, 84, 0], -1)
#             if cnt > 0:
#                 return True, cnt+1
#             else:
#                 return True, 0
#     return False, 0

def main():
    path = '/home/ritz/SpringQ/CV/CVgame/assests/Hands'
    hist_hsv=train_hsv(path)
    print("Hist Created")
    # hist_hsv=np.load("histogram.npy")
    # width, height = 1280, 720
    # cap.set(3, width)
    # cap.set(4, height)
    # cap = cv2.VideoCapture(0)

    # thresh_HSV=0.028
    # while True:
    #     ret, frame = cap.read()
    #     #smoothing of edges
    #     frame = cv2.bilateralFilter(frame, 5, 50, 100)
    #     #mirror flip
    #     frame = cv2.flip(frame, 1)
    #     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #     dst = cv2.calcBackProject([hsv], [0, 1], hist_hsv, [0, 180, 0, 256], 1)
    #     # cv2.imshow('original', dst)
    #     disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    #     cv2.filter2D(dst, -1, disc, dst)
    #     ret, thresh = cv2.threshold(dst, 150, 255, cv2.THRESH_BINARY)
    #     thresh = cv2.merge((thresh, thresh, thresh))
    #     skinMask = cv2.bitwise_and(frame, thresh)
    #     _, conts, hier = cv2.findContours(skinMask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #     max_cont = max(cont, key=cv2.contourArea)
    #     moment = cv2.moments(max_cont)
        # if moment['m00'] != 0:
        #     cx = int(moment['m10'] / moment['m00'])
        #     cy = int(moment['m01'] / moment['m00'])
    #     cv2.circle(frame, cnt_centroid, 5, [255, 0, 255], -1)
    # if max_cont is not None:
    #     hull = cv2.convexHull(max_cont, returnPoints=False)
    #     defects = cv2.convexityDefects(max_cont, hull)
    #     far_point = farthest_point(defects, max_cont, cnt_centroid)
    #     print("Centroid : " + str(cnt_centroid) + ", farthest Point : " + str(far_point))
    #     cv2.circle(frame, far_point, 5, [0, 0, 255], -1)
    #     res = contours[ci]
        # hull = cv2.convexHull(res)
        # drawing = np.zeros(img.shape, np.uint8)
        # cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
        # cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

        # isFinishCal, cnt = calculateFingers(res, drawing)
    #     cv2.imshow('original', cv2.bitwise_and(frame, thresh))
    #     # cv2.imshow("After bilateral filter", frame)
    #     k= cv2.waitKey(10)
    #     if k==27:
    #         break
    # cv2.destroyAllWindows()

if __name__ == '__main__': 
    main()