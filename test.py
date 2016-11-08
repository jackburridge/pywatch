import wx

from pywatch import WatchableDict
from pywatch import wxwatch


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.static_text = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_text.Wrap(-1)

        sizer.Add(self.static_text, 0, wx.ALL | wx.EXPAND, 5)

        self.spin_ctrl = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     wx.SP_ARROW_KEYS, 0, 100, 0)
        sizer.Add(self.spin_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        self.slider = wx.Slider(self, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL)

        sizer.Add(self.slider, 0, wx.ALL | wx.EXPAND, 5)

        self.gauge = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)

        sizer.Add(self.gauge, 0, wx.ALL | wx.EXPAND, 5)

        self.check_box = wx.CheckBox(self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0)

        sizer.Add(self.check_box, 0, wx.ALL, 5)

        self.toggle_btn = wx.ToggleButton(self, wx.ID_ANY, u"Toggle me!", wx.DefaultPosition, wx.DefaultSize, 0)

        sizer.Add(self.toggle_btn, 0, wx.ALL, 5)

        self.text_ctrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)

        sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        self.search_ctrl = wx.SearchCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.search_ctrl.ShowSearchButton(True)
        self.search_ctrl.ShowCancelButton(False)
        sizer.Add(self.search_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        model = WatchableDict()
        model["number"] = 1
        model["bool"] = True
        model["text"] = "text"
        wxwatch.LabelWatcher(self.static_text, (model.get_watcher("number"), model.get_watcher("text")),
                             format="The current number is %s and current text \"%s\".")
        wxwatch.SpinCtrlWatcher(self.spin_ctrl, model.get_watcher("number"))
        wxwatch.SliderWatcher(self.slider, model.get_watcher("number"))
        wxwatch.GaugeWatcher(self.gauge, model.get_watcher("number"))
        wxwatch.CheckBoxWatcher(self.check_box, model.get_watcher("bool"))
        wxwatch.LabelWatcher(self.toggle_btn, (model.get_watcher("number"),), format="Button with number %s.")
        wxwatch.ToggleButtonWatcher(self.toggle_btn, model.get_watcher("bool"))
        wxwatch.TextCtrlWatcher(self.text_ctrl, model.get_watcher("text"))
        wxwatch.TextCtrlWatcher(self.search_ctrl, model.get_watcher("text"))
        wxwatch.EnableWatcher(self.spin_ctrl, model.get_watcher("bool"))


if __name__ == "__main__":
    app = wx.App()
    top = MyFrame(None)
    top.Show()
    app.MainLoop()
