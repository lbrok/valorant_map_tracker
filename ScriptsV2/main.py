import cv2 as cv
import numpy as np
import imagepreprocessing as ipp

img=cv.imread('D:\Scripts\Valtool\Img\IgScreenShots.png',0)
window='Image preview'

crop_img = ipp.crop_p(img,40,60,0.21,0.37)
eq_img = ipp.equalisation(crop_img)
edge_img = ipp.edge(eq_img)

processed_img = np.uint8(0.5*edge_img+0.5*eq_img)

num_rows = np.shape(processed_img)[0]
num_cols = np.shape(processed_img)[1]
threshold = 175
final_img = np.uint8(np.zeros((num_rows,num_cols)))
for i in range(num_rows):
    for j in range(num_cols):
        if processed_img[i,j] < threshold:
            final_img[i,j] = 0
        else:
            final_img[i,j] = processed_img[i,j]


cv.imshow(window, final_img)
cv.waitKey(0)
cv.destroyAllWindows()
