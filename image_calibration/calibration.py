import os
import numpy as np
import cv2
import skimage.io

class calib:
    def calibrate_write(self):
        #Image의 pixel size는 유지하며 보정
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        #criteria : 반복을 종료할 조건(type(종료 조건), 최대 iter, epsilon값(정확도))
        # cv2.TERM_CRITERIA_EPS : 주어진 정확도(epsilon 인자)에 도달하면 반복을 중단
        # cv2.TERM_CRITERIA_MAX_ITER : max_iter 인자에 지정된 횟수만큼 반복하고 중단
        # a + b : 두가지 조건 중 하나가 만족되면 반복 중단

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6*8, 3), np.float32)
        objp[:, :2] = np.mgrid[0:8, 0:6].T.reshape(-1,2)

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

        imgdir = os.path.join(self.py_dir, "check.jpg")
        image = skimage.io.imread(imgdir) # == cv.imread(imgdir)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # gray scale로 변환
        ret, corners = cv2.findChessboardCorners(gray, (8,6), None)

        if ret:
            objpoints.append(objp)

            corners = cv2.cornerSubPix(gray, corners, (11, 11),(-1, -1), criteria) # 찾아진 corners에 대한 보정(corners input/output)
            imgpoints.append(corners)

            cv2.drawChessboardCorners(image, (8,6), corners, ret)
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
            # ret, 카메라 행렬, 왜곡계수, 회전, 이동벡터 반환

            #폴더내의 모든 이미지들의 사이즈가 일정해야 일정하게 왜곡 보정된 이미지를 모두 얻을 수 있음
            for img2 in os.listdir(self.dir):
                if '.jpg' in img2:
                    image_dir_name = os.path.join(self.dir, img2)
                    img = cv2.imread(image_dir_name)
                    # img = cv2.copyMakeBorder(img, 250, 0, 30, 30, cv2.BORDER_CONSTANT, value=[255, 255, 255])
                    # image panning 을 이용하여 왜곡 보정으로 인해 잘리는 부분을 살릴 수 있음
                    h, w = img.shape[:2]
                    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0, (w, h))
                    # image의 카메라 행렬 구체화, 개선(필수사항은 아님)

                    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
                    x,y,w,h = roi
                    dst = dst[y:y+h, x:x+w]

                    # while True:
                    #     cv2.imshow('calibration', dst)
                    #     k = cv2.waitKey(1) & 0xFF
                    #     if k == ord('g'):
                    #         cv2.destroyAllWindows()
                    #         break
                    cv2.imwrite(self.py_dir+'/After_Calibration_image/'+img2, dst)

    def __init__(self, ROOT_DIR):
        self.dir = ROOT_DIR
        self.py_dir = os.getcwd()
        self.calibrate_write()
