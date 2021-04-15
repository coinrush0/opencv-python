import cv2
import numpy as np

def getFilePath(file_name):
    return './image/image_' + file_name + '.png'

def remove_image_shadow(image):
    rgb_planes = cv2.split(image)
    result_planes = []
    # result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        result_planes.append(diff_img)
        # norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        # result_norm_planes.append(norm_img)

    image = cv2.merge(result_planes)
    return image
    
def rectify(h):
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)
    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]
    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]
    return hnew

def scanDocumentImage(image):
    original = image.copy()

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

    # blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # edged_image = cv2.Canny(image, 50, 100)
    # original_edged = edged_image.copy()
    # cv2.imwrite(getFilePath("original_"), original_edged)
    (contours, _) = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    p = cv2.arcLength(contours[0], True)
    approx = cv2.approxPolyDP(contours[0], 0.02 * p, True)
    cv2.drawContours(image, approx, -1, (0, 255, 0), 3)

    for c in contours:
        p = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * p, True)

        if len(approx) == 4:
            target = approx
            break

    approx = rectify(target)
    pts2 = np.float32([[0,0],[800,0],[800,800],[0,800]])
    M = cv2.getPerspectiveTransform(approx,pts2)
    final_image = cv2.warpPerspective(original,M,(800,800))
    return cv2.cvtColor(final_image, cv2.COLOR_BGR2GRAY)