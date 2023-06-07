"""This program takes information about the pixels within the selected ROI and creates a HS histogram."""
import cv2
import numpy as np
import matplotlib.pyplot as plt

"""Takes 10 selected ROI images in HSI and creates a normalized histogram for the users skin color."""
def create_hist():
    # Size of the screen/window
    width, height = 1280, 720
    # Getting feed from webcam
    capture = cv2.VideoCapture(0)
    capture.set(3, width)
    capture.set(4, height)
    # List of images captured by the ROI selection
    list_roi=[]
    # Count for number of ROI's selected
    count=0
    while capture.isOpened():
        # getting the frames from webcam input
        suc, frame = capture.read()
        # When key is pressed
        key = cv2.waitKey(1)
        # Does a horizontal flip, so that the left and right are same on screen
        img = cv2.flip(frame, 1)
        # Converts the BGR to HSI color
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # When a key is pressed and it is the character 'z'
        if pressed_key & 0xFF == ord('z'):
            # Checks if 10 counts of ROI have been selected
            if count<11:
                corners = cv2.selectROI(img)
                cv2.destroyAllWindows()
                # Get position and dimensions of the selected ROI rectangle
                x, y, w, h = corners
                roi = np.zeros([w, h, 3], dtype=hsv.dtype)
                # Get the information from the HSI image for the given ROI rectangle dimensions
                roi = hsv[x:x+w, y:y+h]
                list_roi.append(roi)
                count+=1
        cv2.imshow("Get Skin Color", img)
        k = cv2.waitKey(10)
        if k==27:
            break
        if count>=10:
            break
    cv2.destroyAllWindows()
    # create histogram for color channels H and S
    hist=cv2.calcHist(list_roi, [0, 1], None, [180, 256], [0, 180, 0, 256])
    norm=cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    # Save and show the histogram
    np.save("histogram.npy", norm)
    plt.imshow(norm)
    plt.colorbar()
    plt.show()

if __name__ == '__main__': 
    create_hist()
