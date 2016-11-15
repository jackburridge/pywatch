import wx

import pywatch.wx
from pywatch import WatchableDict


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=u"My Frame")

        self.model = WatchableDict()
        self.model["text"] = ""

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.text_ctrl, 0, 0, 0)
        pywatch.wx.TextCtrlWatcher(self.text_ctrl, self.model, "text")

        self.static_text = wx.StaticText(self, wx.ID_ANY, u"Text: {0}", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.static_text, 0, 0, 0)
        pywatch.wx.LabelWatcher(self.static_text, self.model, ["text"])

        self.SetSizer(sizer)

        self.Centre(wx.BOTH)


if __name__ == "__main__":
    app = wx.App()
    top = MyFrame(None)
    top.Show()
    app.MainLoop()
