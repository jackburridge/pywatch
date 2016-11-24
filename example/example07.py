import wx

import pywatch.wx
from pywatch import WatchableDict


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"List Editor", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        sizer = wx.BoxSizer(wx.VERTICAL)

        gb_sizer = wx.GridBagSizer(5, 5)
        gb_sizer.SetFlexibleDirection(wx.BOTH)
        gb_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        list_boxChoices = []
        self.list_box = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, list_boxChoices, 0)
        gb_sizer.Add(self.list_box, wx.GBPosition(0, 0), wx.GBSpan(1, 2), wx.EXPAND, 0)

        self.add_button = wx.Button(self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0)
        gb_sizer.Add(self.add_button, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.EXPAND, 0)

        self.remove_button = wx.Button(self, wx.ID_ANY, u"Remove", wx.DefaultPosition, wx.DefaultSize, 0)
        gb_sizer.Add(self.remove_button, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.EXPAND, 0)

        self.text_ctrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gb_sizer.Add(self.text_ctrl, wx.GBPosition(2, 0), wx.GBSpan(1, 2), wx.EXPAND, 0)

        gb_sizer.AddGrowableCol(0)
        gb_sizer.AddGrowableCol(1)
        gb_sizer.AddGrowableRow(0)

        sizer.Add(gb_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.add_button.Bind(wx.EVT_BUTTON, self.on_add)
        self.remove_button.Bind(wx.EVT_BUTTON, self.on_remove)

        self.model = WatchableDict()
        self.model["list"] = ["one", "two", "three", "four"]
        self.model["selection"] = 0

        pywatch.wx.ItemContainerItemWatcher(self.list_box, self.model, "list")
        pywatch.wx.SelectionChanger(self.list_box, self.model, "selection")

        def getter():
            return self.model["list"][self.model["selection"]]

        def setter(value):
            self.model["list"][self.model["selection"]] = value

        pywatch.wx.ValueChanger(self.text_ctrl, self.model, ("list", "selection", setter, getter))

    def on_add(self, event):
        self.model["list"].append(self.model["list"][self.model["selection"]])
        event.Skip()

    def on_remove(self, event):
        self.model["list"].pop(self.model["selection"])
        event.Skip()


if __name__ == "__main__":
    app = wx.App()
    top = MyFrame(None)
    top.Show()
    app.MainLoop()
