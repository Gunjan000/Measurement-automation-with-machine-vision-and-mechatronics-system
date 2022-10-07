import cv2
from object_detector import *
import numpy as np
import time

# Load Aruco detector
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)


# Load Object Detector
detector = HomogeneousBgDetector()

# Load Cap
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1990/2)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080/2)

#LOADING CALIBRATED CAMERA MATRIX

mtx= np.load(r"C:\Users\Admin\Desktop\INTERNSHIP\Designs\gauge\measure_object_size\calibration variables\mtx.npy")
dist= np.load(r"C:\Users\Admin\Desktop\INTERNSHIP\Designs\gauge\measure_object_size\calibration variables\dist.npy")
rvecs= np.load(r"C:\Users\Admin\Desktop\INTERNSHIP\Designs\gauge\measure_object_size\calibration variables\rvecs.npy")
tvecs= np.load(r"C:\Users\Admin\Desktop\INTERNSHIP\Designs\gauge\measure_object_size\calibration variables\tvecs.npy")
objpoints= np.load(r"C:\Users\Admin\Desktop\INTERNSHIP\Designs\gauge\measure_object_size\calibration variables\objpoints.npy")
imgpoints = np.load(r"C:\Users\Admin\Desktop\INTERNSHIP\Designs\gauge\measure_object_size\calibration variables\imgpoints.npy")


while True:
    _, img = cap.read()

    h,  w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    
    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w] ################## distoration free     
    # undistort
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]################## cropped
    
    # Get Aruco marker
    corners, _, _ = cv2.aruco.detectMarkers(dst, aruco_dict, parameters=parameters)
    if corners:

        # Draw polygon around the marker
        int_corners = np.int0(corners)
        cv2.polylines(dst, int_corners, True, (0, 255, 0), 1)

        # Aruco Perimeter
        aruco_perimeter = cv2.arcLength(corners[0], True)

        # Pixel to cm ratio
        pixel_cm_ratio = aruco_perimeter / 77.15
        contours = detector.detect_objects(dst)

        # Draw objects boundaries
        for cnt in contours:
            # Get rect
            rect = cv2.minAreaRect(cnt)
            (x, y), (w, h), angle = rect

            # Get Width and Height of the Objects by applying the Ratio pixel to cm
            object_width = w / pixel_cm_ratio
            object_height = h / pixel_cm_ratio

            # Display rectangle
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            cv2.circle(dst, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv2.polylines(dst, [box], True, (255, 0, 0), 1)
            cv2.putText(dst, "Width {} mm".format(round(object_width, 4)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            cv2.putText(dst, "Height {} mm".format(round(object_height, 4)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    img= cv2.resize(dst, (0, 0), None, 0.5, 0.5)

 #   time.sleep(1)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()