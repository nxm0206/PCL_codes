# cv2.cvtColor takes a numpy ndarray as an argument
import numpy as np

import wx

# importing OpenCV
import cv2

from PIL import ImageGrab


def screen_record(left, top, right, bottom):

        cap = ImageGrab.grab(bbox=(left, top, right, bottom))

        recorded_gray = cv2.cvtColor(np.array(cap), cv2.COLOR_BGR2GRAY)

        return recorded_gray


# Calling the function


class FancyFrame(wx.Frame):
    def __init__(self, x0, y0, width, height):
        wx.Frame.__init__(self, None, style = wx.STAY_ON_TOP |wx.FRAME_NO_TASKBAR |wx.FRAME_SHAPED, pos=(x0, y0), size=(width, height))
        self.SetTransparent(100)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyDown)
        self.Show(True)

    def OnKeyDown(self, event):
        """quit if user press Esc"""
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close(force=True)
        else:
            event.Skip()

def display_RecRegion(x0, y0, width, height):
    app = wx.App()
    FancyFrame(x0, y0, width, height)
    app.MainLoop()

if __name__ == "__main__":
    x0 = 300
    y0 = 300
    width = 320
    height = 256

    # display_RecRegion(x0, y0, width, height)

    captured = screen_record(x0*1.25, y0*1.25, (x0+width)*1.25-1, (y0+height)*1.25-1)


    print((captured))


    cv2.imshow('imshow', captured)
    cv2.waitKey(0)
    print(captured)


# screen_record()