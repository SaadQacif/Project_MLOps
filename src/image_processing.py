import cv2
import numpy as np
import matplotlib.pyplot as plt

def hist_monochrome(x):
    buckets = [0 for _ in range(256)]
    labels = np.array([i for i in range(256)])

    for i in x:
        buckets[int(i)] += 1

    return labels, np.array(buckets)

def contour(im_arr, threshold=70, gray=False):
    if gray:
        gr_im_arr = im_arr
    else:
        gr_im_arr = np.sum(im_arr, axis=2) / 3

    kernel = np.array([
                          [1, 1, 1],
                          [1, 1, 1],
                          [1, 1, 1],
                      ], dtype=np.uint8)
    dst = cv2.dilate(gr_im_arr, kernel, iterations=1)
    dst = cv2.erode(gr_im_arr, kernel, iterations=1)
    kernel = np.array([
                          [0., -1., 0.],
                          [-1., 4., -1.],
                          [0., -1., 0.],
                      ])
    dst = cv2.filter2D(dst, -1, np.flip(kernel))
    dst = np.clip(np.floor(dst), 0, 255)


    dst = (dst >= threshold) * 255

    return dst

img = cv2.imread('inputs/healthy_2.png', cv2.IMREAD_COLOR)
assert img is not None, "file could not be read, check with os.path.exists()"
 
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
# Convert to LAB
lab_im = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
# Apply CLAHE to lightness channel
lab_im[:, :, 0] = clahe.apply(lab_im[:, :, 0])
# Convert back to RGB
img = cv2.cvtColor(lab_im, cv2.COLOR_LAB2RGB)
# img = contour(img)

cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# cv2.imwrite('inputs/clahe_2.png',img)
