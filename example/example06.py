import wx

import pywatch.wx
from pywatch import WatchableDict


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=u"Addition Frame")

        self.model = WatchableDict()
        self.model["a"] = 0
        self.model["b"] = 0

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        sizer = wx.BoxSizer(wx.VERTICAL)

        gb_sizer = wx.GridBagSizer(5, 5)
        gb_sizer.SetFlexibleDirection(wx.BOTH)
        gb_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.spin_ctrl_a = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.SP_ARROW_KEYS, 0, 10, 0)
        gb_sizer.Add(self.spin_ctrl_a, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                     wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)
        pywatch.wx.SpinCtrlWatcher(self.spin_ctrl_a, self.model, "a")

        self.static_text = wx.StaticText(self, wx.ID_ANY, u"+", wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_text.Wrap(-1)
        gb_sizer.Add(self.static_text, wx.GBPosition(0, 1), wx.GBSpan(1, 1),
                     wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.spin_ctrl_b = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.SP_ARROW_KEYS, 0, 10, 0)
        gb_sizer.Add(self.spin_ctrl_b, wx.GBPosition(0, 2), wx.GBSpan(1, 1),
                     wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        pywatch.wx.SpinCtrlWatcher(self.spin_ctrl_b, self.model, "b")

        self.static_text_out = wx.StaticText(self, wx.ID_ANY, u"{}", wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_text_out.Wrap(-1)
        gb_sizer.Add(self.static_text_out, wx.GBPosition(1, 0), wx.GBSpan(1, 3),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        pywatch.wx.LabelWatcher(self.static_text_out, self.model, ("a", "b", lambda a, b: a + b))

        self.gauge = wx.Gauge(self, wx.ID_ANY, 20, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.gauge.SetValue(0)
        gb_sizer.Add(self.gauge, wx.GBPosition(2, 0), wx.GBSpan(1, 3),
                     wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        pywatch.wx.ValueWatcher(self.gauge, self.model, ("a", "b", lambda a, b: a + b))

        gb_sizer.AddGrowableCol(0)
        gb_sizer.AddGrowableCol(2)

        sizer.Add(gb_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()

        self.Centre(wx.BOTH)


if __name__ == "__main__":
    app = wx.App()
    top = MyFrame(None)
    top.Show()
    app.MainLoop()
