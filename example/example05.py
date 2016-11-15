import wx

import pywatch.wx
from pywatch import WatchableDict


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Selection Frame", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        sizer = wx.BoxSizer(wx.VERTICAL)

        gb_sizer = wx.GridBagSizer(5, 5)
        gb_sizer.SetFlexibleDirection(wx.BOTH)
        gb_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        choices = [u"One", u"Two", u"Three"]
        self.combo_box = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     choices, 0)
        gb_sizer.Add(self.combo_box, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.EXPAND, 5)

        self.choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choices, 0)
        self.choice.SetSelection(0)
        gb_sizer.Add(self.choice, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.EXPAND, 5)

        self.list_box = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choices, 0)
        gb_sizer.Add(self.list_box, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.EXPAND, 5)

        self.radio_box = wx.RadioBox(self, wx.ID_ANY, u"Radio Box", wx.DefaultPosition, wx.DefaultSize,
                                     choices, 1, wx.RA_SPECIFY_COLS)
        self.radio_box.SetSelection(0)
        gb_sizer.Add(self.radio_box, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.EXPAND, 5)

        gb_sizer.AddGrowableCol(0)
        gb_sizer.AddGrowableRow(2)

        sizer.Add(gb_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()

        self.Centre(wx.BOTH)
        self.model = WatchableDict()
        self.model["selection"] = 1

        pywatch.wx.ListBoxWatcher(self.list_box, self.model, "selection")
        pywatch.wx.RadioBoxWatcher(self.radio_box, self.model, "selection")
        pywatch.wx.ChoiceWatcher(self.choice, self.model, "selection")
        pywatch.wx.ComboBoxWatcher(self.combo_box, self.model, "selection")


if __name__ == "__main__":
    app = wx.App()
    top = MyFrame(None)
    top.Show()
    app.MainLoop()
