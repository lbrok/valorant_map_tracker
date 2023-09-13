import cv2 as cv
import numpy as np
import time

class Tracker:

    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):

        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

        self.method = method


    def FindPortraits(self, haystack_img, threshold=0.9, debug_mode=None):

        time.sleep(0.2)
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        locations=np.where(result >= threshold)
        locations=list(zip(*locations[::-1]))

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect) #Duplicate rectangles to make sure no results are removed when grouped
        rectangles , weights = cv.groupRectangles(rectangles, 1, 0.5)

        points=[]
        if locations:

            line_color = (0, 255, 239)
            line_type = cv.LINE_4
            thickness=1

            for (x,y,w,h) in rectangles:
                center=(int(x+w/2-1),int(y+w/2-1))
                points.append(center)

                if debug_mode == "circle":
                    cv.circle(haystack_img,center,w+3,line_color,thickness,line_type)

        if debug_mode:
            cv.imshow("Result",haystack_img)
            #cv.waitKey()

        return points
