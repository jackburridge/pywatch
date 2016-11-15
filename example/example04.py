import datetime
import thread
import time
import wx

import pywatch.wx
from pywatch import WatchableDict


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Background Logging", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        sizer = wx.BoxSizer(wx.VERTICAL)

        gb_sizer = wx.GridBagSizer(5, 5)
        gb_sizer.SetFlexibleDirection(wx.BOTH)
        gb_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        list_boxChoices = []
        self.list_box = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, list_boxChoices, 0)
        gb_sizer.Add(self.list_box, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.EXPAND, 0)

        self.button = wx.Button(self, wx.ID_ANY, u"Run", wx.DefaultPosition, wx.DefaultSize, 0)
        gb_sizer.Add(self.button, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.EXPAND, 0)

        gb_sizer.AddGrowableCol(0)
        gb_sizer.AddGrowableRow(0)

        sizer.Add(gb_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.button.Bind(wx.EVT_BUTTON, self.on_run)

        self.model = WatchableDict()
        self.model["logs"] = []
        pywatch.wx.ItemContainerItemWatcher(self.list_box, self.model, "logs")



        # Virtual event handlers, overide them in your derived class
    def on_run(self, event):
        thread.start_new_thread(self.background_task, ())
        event.Skip()

    def background_task(self):
        while True:
            self.model["logs"].append(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
            time.sleep(0.5)


if __name__ == "__main__":
    app = wx.App()
    top = MyFrame(None)
    top.Show()
    app.MainLoop()
