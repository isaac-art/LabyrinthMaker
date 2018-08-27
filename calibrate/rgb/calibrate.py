import numpy as np
import cv2
import glob    
import json

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*10,3), np.float32)
objp[:,:2] = np.mgrid[0:10,0:7].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('*.png')
c = 0

# images captured by saveTestImages.py
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (10, 7), None)

    # If found, add object points, image points
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (10, 7), corners2,ret)
        cv2.imshow('img',img)
        cv2.imwrite('checks/calib_%s.png' % c, img)
        # cv2.waitKey(500)

    c = c + 1


ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

# SAVE TO FILE
# save the matrix and distortion to csv files for easy viewing
np.savetxt('mtx.csv', mtx, delimiter=',')
np.savetxt('dist.csv', dist, delimiter=',')
# save the rest to numpy files as it is multidimensional
np.save('rvecs.npy', rvecs)
np.save('tvecs.npy', tvecs)

# TEST  UNDISTORT
img = cv2.imread('14_copy.png')
h,  w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
print(roi)

# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
# crop the image to roi
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('calibresult_0.png', dst)


cv2.destroyAllWindows()