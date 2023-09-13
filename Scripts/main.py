import cv2 as cv
import numpy as np
import time
from windowcapture import WindowCapture
from tracker import Tracker
from ocr import OCR

wincap=WindowCapture("round")
roundcounter=OCR()
tracker_sova=Tracker('D:\Scripts\Valtool\Img\IMG_Sova.jpg')
#tracker_astra=Tracker('D:\Scripts\Valtool\Img\IMG_Astra.jpg')

loop_time=time.time()
while wincap:

    screenshot = wincap.get_screenshot()

    roundnumber = roundcounter.FindRound(screenshot, 0.75)

    #cv.imshow("Screen Capture", screenshot)
    point=tracker_sova.FindPortraits(screenshot, 0.67, debug_mode="circle")
    #tracker_astra.FindPortraits(screenshot, 0.6, debug_mode="circle")

    print(f'FPS {1/(time.time()-loop_time)} Round: {roundnumber}')
    #print(f'FPS {1/(time.time()-loop_time)}, Antal cirklar: {len(point)}, Positioner: {point}')
    loop_time = time.time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


#avatars=FindPortraits('D:\Scripts\Valtool\Img\IMG_Sova.jpg', "D:\Scripts\Valtool\Img\IMG_Big.jpg", debug_mode="circle")

#WindowCapture()
