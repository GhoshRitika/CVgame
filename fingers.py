import cv2
import numpy as np
import math

"""This class detects and tracks fingers using histogram base skin color segmentation."""
class Finger:
    def __init__(self):
        # Loading previously saved histogram
        self.hist_hsv =np.load("histogram.npy")
    """
    # Reference
    # Author: Ankush Bhatia
    # github link : https://github.com/ankushbhatia2/finger_detect_opencv_python/blob/master/hand_detect.py
    Calculates the number of fingers that are upright, given the number of defects
    :param defects The protrusions or anamolies in the convex hull
    :param max The contour with the maximum area
    :return Number of fingers that are upright
    """
    def calculateFingers(self, defects, max):
        count = 0
        # loop thorugh all the defects
        for i in range(defects.shape[0]):
            s, e, f, _ = defects[i][0]
            starting_pt = tuple(max[s][0])
            ending_pt = tuple(max[e][0])
            farthest_pt = tuple(max[f][0])
            # calculating the 3 sides of the triangle made by the defect
            A = ((ending_pt[0] - starting_pt[0]) ** 2 + (ending_pt[1] - starting_pt[1]) ** 2)**0.5
            B = ((farthest_pt[0] - starting_pt[0]) ** 2 + (farthest_pt[1] - starting_pt[1]) ** 2)**0.5
            C = ((ending_pt[0] - farthest_pt[0]) ** 2 + (ending_pt[1] - farthest_pt[1]) ** 2)**0.5
            # using cosine theorem to find the angle between defect starting and ending point
            angle = math.acos((B ** 2 + C ** 2 - A ** 2) / (2 * C * B))  
            # angle less than 90 degree, treat as fingers
            if angle<math.pi/2:
                count += 1
        if count > 0:
            return count+1
        else:
            return 0
    """
    Calculates the farthest contour point from the centroid of the maximun contour area
    :param max The contour with the maximum area
    :param centroid The position of the centroid of the max contour
    :param defects The protrusions or anamolies in the convex hull
    :return The position of the farthest contour point from the centroid of the contour
    """
    def find_farthest_point(self, max, centroid, defects):
        centroid_x, centroid_y = centroid
        max_dist = -1
        farthest_point = None
        for i in range(defects.shape[0]):
            s, _, _, _ = defects[i][0]
            start = tuple(max[s][0])
            distance = math.sqrt((start[0] - centroid_x) ** 2 + (start[1] - centroid_y) ** 2)
            if distance > max_dist:
                max_dist = distance
                farthest_point = start
        return farthest_point

    """
    Detect a hand and its fingers using histogram based skin color segmentation
    :param frames The image from which a finger is to be detected
    :return The position of the farthest contour point from the centroid of the contour
    :return Number of fingers that are upright
    """
    def detect_fingers(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Calculating the back projection of the HSV image based on the skin color histogram
        back_proj = cv2.calcBackProject([hsv], [0, 1], self.hist_hsv, [0, 180, 0, 256], 1)
        # 2D convolution with the SE to enhance the back projection
        SE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
        cv2.filter2D(back_proj, -1, SE, back_proj)
        # thresholding at 150 to get a filtered binary image
        ret, thresh = cv2.threshold(back_proj, 150, 255, cv2.THRESH_BINARY)
        thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        # Create a kernel for erosion
        kernel = np.ones((3, 3), np.uint8)
        # Performing opening to smoothen the mask by removing noise
        thresh = cv2.erode(thresh, kernel, iterations=2)
        thresh = cv2.dilate(thresh, kernel, iterations=2)
        # Keeps only the frame pixels from the masked image with non zero values
        masked_img = cv2.bitwise_and(frame, thresh)
        # Only for visualization
        # cv2.imshow("original", masked_img)
        # Get a list of contours
        gray_img = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
        contour_list, hierarchy = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Find the area with the maximum contour area
        max_cont = None
        length = len(contour_list)
        maxArea = -1
        if length > 0:
            for i in range(length):
                temp = contour_list[i]
                area = cv2.contourArea(temp)
                if area > maxArea:
                    maxArea = area
                    ci = i
            max_cont = contour_list[ci]
            # This part is for visualization purposes
            # Get the convex hull and draw the max contour and hull on a blank screen
            hull = cv2.convexHull(max_cont)
            drawing = np.zeros(masked_img.shape, np.uint8)
            cv2.drawContours(drawing, [max_cont], 0, (0, 255, 0), 2)
            cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)
            #only for visualizing
            # cv2.imshow("output", drawing)
            # Calculate the centroid of the max contour area
            M = cv2.moments(max_cont)
            centroid_x = int(M["m10"] / M["m00"])
            centroid_y = int(M["m01"] / M["m00"])
            centroid = centroid_x, centroid_y
            # Get indices of the contour points that form the convex hull.
            hull = cv2.convexHull(max_cont, returnPoints=False)
            # Get the deviations or concave parts of the max contour are
            defects = cv2.convexityDefects(max_cont, hull)
            if defects is not None:
                # Calculate the position of the point farthest from the centroid
                far_point = self.find_farthest_point(max_cont, centroid, defects)
                # Calculate the number of defects that could be fingers
                count_fin = self.calculateFingers(defects, max_cont)
                # Draw a purple filled circle at the centroid of max contour area
                cv2.circle(frame, centroid, 7, [255, 0, 255], -1)
                # Draw a red filled circle at the farthest point from the centroid of max contour area
                cv2.circle(frame, far_point, 7, [0, 0, 255], -1)
                return far_point, count_fin

# if __name__ == '__main__': 
#     # Size of the screen/window
#     width, height = 1280, 720
#     # Getting feed from webcam
#     capture = cv2.VideoCapture(0)
#     capture.set(3, width)
#     capture.set(4, height)
#     finger = Finger()
#     while capture.isOpened():
#         # getting the frames from webcam input
#         suc, frame = capture.read()
#         # Does a horizontal flip, so that the left and right are same on screen
#         img = cv2.flip(frame, 1)
#         far, cnt = finger.detect_fingers(img)
#         cv2.imshow("Live Feed", img)
#         k = cv2.waitKey(10)
#         if k==27:
#             break
#     cv2.destroyAllWindows()