import cv2
import numpy as np
import math

class Finger:
    def __init__(self):
        # self.frame = frame
        self.hand_hist = hist_hsv=np.load("histogram.npy")
        self.traverse_point = []
        self.total_rectangle = 9
        self.hand_rect_one_x = None
        self.hand_rect_one_y = None
        self.hand_rect_two_x = None
        self.hand_rect_two_y = None

    def calculateFingers(self, res, drawing):
        #  convexity defect
        hull = cv2.convexHull(res, returnPoints=False)
        if len(hull) > 3:
            defects = cv2.convexityDefects(res, hull)
            if defects is not None:
                cnt = 0
                for i in range(defects.shape[0]):  # calculate the angle
                    s, e, f, d = defects[i][0]
                    start = tuple(res[s][0])
                    end = tuple(res[e][0])
                    far = tuple(res[f][0])
                    a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                    b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                    c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                    angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
                    if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                        cnt += 1
                        cv2.circle(drawing, far, 8, [211, 84, 0], -1)
                if cnt > 0:
                    return True, cnt+1
                else:
                    return True, 0
        return False, 0

    def rescale_frame(self, frame, wpercent=130, hpercent=130):
        width = int(frame.shape[1] * wpercent / 100)
        height = int(frame.shape[0] * hpercent / 100)
        return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

    def contours(self, hist_mask_image):
        gray_hist_mask_image = cv2.cvtColor(hist_mask_image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_hist_mask_image, 0, 255, 0)
        cont, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return cont

    def draw_rect(self, frame):
        rows, cols, _ = frame.shape
        self.hand_rect_one_x = np.array(
            [6 * rows / 20, 6 * rows / 20, 6 * rows / 20, 9 * rows / 20, 9 * rows / 20, 9 * rows / 20, 12 * rows / 20,
             12 * rows / 20, 12 * rows / 20], dtype=np.uint32)

        self.hand_rect_one_y = np.array(
            [9 * cols / 20, 10 * cols / 20, 11 * cols / 20, 9 * cols / 20, 10 * cols / 20, 11 * cols / 20, 9 * cols / 20,
             10 * cols / 20, 11 * cols / 20], dtype=np.uint32)

        self.hand_rect_two_x = self.hand_rect_one_x + 10
        self.hand_rect_two_y = self.hand_rect_one_y + 10

        for i in range(self.total_rectangle):
            cv2.rectangle(frame, (self.hand_rect_one_y[i], self.hand_rect_one_x[i]),
                          (self.hand_rect_two_y[i], self.hand_rect_two_x[i]),
                          (0, 255, 0), 1)

        return frame

    def hand_histogram(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        roi = np.zeros([90, 10, 3], dtype=hsv_frame.dtype)

        for i in range(self.total_rectangle):
            roi[i * 10: i * 10 + 10, 0: 10] = hsv_frame[self.hand_rect_one_x[i]:self.hand_rect_one_x[i] + 10,
                                              self.hand_rect_one_y[i]:self.hand_rect_one_y[i] + 10]

        hand_hist = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
        norm = cv2.normalize(hand_hist, hand_hist, 0, 255, cv2.NORM_MINMAX)
        np.save("histogram.npy", norm)
        return norm

    def hist_masking(self, frame, hist):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
        cv2.filter2D(dst, -1, disc, dst)

        ret, thresh = cv2.threshold(dst, 150, 255, cv2.THRESH_BINARY)
        thresh = cv2.merge((thresh, thresh, thresh))
        # cv2.namedWindow('original', cv2.WINDOW_NORMAL)
        # window_size = (800, 600)
        # cv2.resizeWindow('original', *window_size)
        # cv2.imshow("Output", drawing)
        # cv2.imshow('original', cv2.bitwise_and(frame, thresh))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return cv2.bitwise_and(frame, thresh)

    def centroid(self, max_contour):
        moment = cv2.moments(max_contour)
        if moment['m00'] != 0:
            cx = int(moment['m10'] / moment['m00'])
            cy = int(moment['m01'] / moment['m00'])
            return cx, cy
        else:
            return None

    def farthest_point(self, defects, contour, centroid):
        if defects is not None and centroid is not None:
            s = defects[:, 0][:, 0]
            cx, cy = centroid

            x = np.array(contour[s][:, 0][:, 0], dtype=np.float64)
            y = np.array(contour[s][:, 0][:, 1], dtype=np.float64)

            xp = cv2.pow(cv2.subtract(x, cx), 2)
            yp = cv2.pow(cv2.subtract(y, cy), 2)
            dist = cv2.sqrt(cv2.add(xp, yp))

            dist_max_i = np.argmax(dist)

            if dist_max_i < len(s):
                farthest_defect = s[dist_max_i]
                farthest_point = tuple(contour[farthest_defect][0])
                return farthest_point
            else:
                return None

    def draw_circles(self, frame, traverse_point):
        if traverse_point is not None:
            for i in range(len(traverse_point)):
                cv2.circle(frame, traverse_point[i], int(5 - (5 * i * 3) / 100), [0, 255, 255], -1)

    def manage_image_opr(self, frame):
        
        hist_mask_image = self.hist_masking(frame, self.hand_hist)

        hist_mask_image = cv2.erode(hist_mask_image, None, iterations=2)
        hist_mask_image = cv2.dilate(hist_mask_image, None, iterations=2)

        contour_list = self.contours(hist_mask_image)
        max_cont = max(contour_list, key=cv2.contourArea)
        length = len(contour_list)
        maxArea = -1
        if length > 0:
            for i in range(length):
                temp = contour_list[i]
                area = cv2.contourArea(temp)
                if area > maxArea:
                    maxArea = area
                    ci = i
            res = contour_list[ci]
            hull = cv2.convexHull(res)
            drawing = np.zeros(hist_mask_image.shape, np.uint8)
            cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
            cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)
            isFinish, count = self.calculateFingers(res, drawing)
            # cv2.imshow("Output", drawing)
        cnt_centroid = self.centroid(max_cont)
        cv2.circle(frame, cnt_centroid, 5, [255, 0, 255], -1)

        if max_cont is not None:
            hull = cv2.convexHull(max_cont, returnPoints=False)
            defects = cv2.convexityDefects(max_cont, hull)
            far_point = self.farthest_point(defects, max_cont, cnt_centroid)
            # print("Centroid : " + str(cnt_centroid) + ", farthest Point : " + str(far_point))
            cv2.circle(frame, far_point, 5, [0, 0, 255], -1)
            if len(self.traverse_point) < 20:
                self.traverse_point.append(far_point)
            else:
                self.traverse_point.pop(0)
                self.traverse_point.append(far_point)
            print("count : " + str(count) + ", farthest Point : " + str(far_point))
            return far_point, count

# if __name__ == '__main__':
#     capture = cv2.VideoCapture(0)

#     while True:
#         _, frame = capture.read()
#         frame = cv2.flip(frame, 1)
#         finger = Finger()
#         far, cnt = finger.manage_image_opr(frame)
#         print("count : " + str(cnt) + ", farthest Point : " + str(far))
#         cv2.imshow("Live Feed", finger.rescale_frame(frame))
#         k= cv2.waitKey(10)
#         if k==27:
#             break

#     cv2.destroyAllWindows()
#     capture.release()