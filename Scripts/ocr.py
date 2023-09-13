import cv2 as cv
import numpy as np

class OCR:
    def __init__(self, method=cv.TM_CCOEFF_NORMED):

        #Loading all images
        self.imagenames = ["zero.jpg", "one.jpg", "two.jpg", "three.jpg", "four.jpg",
        "five.jpg", "six.jpg", "seven.jpg", "eight.jpg", "nine.jpg"]
        self.images = []
        for self.name in self.imagenames:
            self.img = cv.imread(f'D:\\Scripts\\Valtool\\Img\\Nr\\{self.name}', cv.IMREAD_UNCHANGED)
            self.images.append(self.img)

        self.needle_w = 10
        self.needle_h = 10

        self.method = method

    def FindRound(self, haystack_img, threshold=0.9, debug_mode=None):

        round=0

        for count, number in enumerate(self.images):
            numbermatch=cv.matchTemplate(haystack_img, number, self.method)
            locations=np.where(numbermatch >= threshold)
            locations=list(zip(*locations[::-1]))

            if locations:
                print(locations, count)
                round=round+count

        return round
