import numpy as np
import cv2
import glob

cboard_width = 9
cboard_height = 6
cboard_square_size = 35.0

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

cboard_3D_points = np.zeros((cboard_width * cboard_height, 3), np.float32)
cboard_3D_points[:,:2] = np.mgrid[0:cboard_width, 0:cboard_height].T.reshape(-1,2)*cboard_square_size

list_cboard_3D_points = []
list_cboard_2D_img_points = []

list_images = glob.glob('*jpg')

for frame_name in list_images:
    img = cv2.imread(frame_name)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ret, corners = cv2.findChessboardCorners(gray, (9,6), None)
    
    if ret == True:
        list_cboard_3D_points.append(cboard_3D_points)
        
        corners_in_image = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        list_cboard_2D_img_points.append(corners_in_image)
        
        cv2.drawChessboardCorners(img, (cboard_width, cboard_height), corners_in_image, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)
        
cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(list_cboard_3D_points, list_cboard_2D_img_points, gray.shape[::-1], None, None)

print("Calibration Matrix: ")
print(mtx)
print(f"Distortion: {dist}")

with open('camera_calibration.npy', 'wb') as f:
    np.save(f, mtx)
    np.save(f, dist)
