import win32gui, win32ui, win32con
import numpy as np

class WindowCapture:

    def __init__(self, region):#, window_name)

        if region == "map":
            self.hwnd = None

        #Kan modifiera kommaterade delar till att bara spela in ett visst fönster. Ta bort rad self.hwnd = None i såna fall
        #self.hwnd =win32gui.FindWindow(None, window_name)
        #if not self.hwnd:
            #raise Exception(f"Window not found: {window_name}")
            self.w = 380
            self.h = 380
            self.cropx = 40
            self.cropy = 40

        elif region == "round":
            self.hwnd = None
            self.w = 24
            self.h = 20
            self.cropx = int(1920/2-self.w/2+27)
            self.cropy = 0

    def get_screenshot(self):

        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w,self.h),dcObj, (self.cropx,self.cropy), win32con.SRCCOPY)
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        #Free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        #Removing alpha-channel
        img = img[...,:3]
        #To avoid more errors
        img = np.ascontiguousarray(img)

        return img

    def get_screen_position(self, pos):
        return (pos[0] + self.cropx, pos[1] + self.cropy)
