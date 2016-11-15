import wx

import pywatch.wx
from pywatch import WatchableDict


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"List Frame", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        sizer = wx.BoxSizer(wx.VERTICAL)

        gb_sizer = wx.GridBagSizer(5, 5)
        gb_sizer.SetFlexibleDirection(wx.BOTH)
        gb_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        list_boxChoices = []
        self.list_box = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, list_boxChoices, 0)
        gb_sizer.Add(self.list_box, wx.GBPosition(0, 0), wx.GBSpan(1, 2), wx.EXPAND, 0)

        combo_boxChoices = []
        self.combo_box = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     combo_boxChoices, 0)
        gb_sizer.Add(self.combo_box, wx.GBPosition(1, 0), wx.GBSpan(1, 2), wx.EXPAND, 0)

        choiceChoices = []
        self.choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choiceChoices, 0)
        self.choice.SetSelection(0)
        gb_sizer.Add(self.choice, wx.GBPosition(2, 0), wx.GBSpan(1, 2), wx.EXPAND, 0)

        self.text_ctrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     wx.TE_PROCESS_ENTER)
        gb_sizer.Add(self.text_ctrl, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.EXPAND, 0)

        self.button = wx.Button(self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0)
        gb_sizer.Add(self.button, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 0)

        gb_sizer.AddGrowableCol(0)
        gb_sizer.AddGrowableRow(0)

        sizer.Add(gb_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.button.Bind(wx.EVT_BUTTON, self.on_add)
        self.text_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_add)

        self.model = WatchableDict()
        self.model["list"] = []
        pywatch.wx.TextCtrlWatcher(self.text_ctrl, self.model, "text")
        pywatch.wx.ItemContainerItemWatcher(self.list_box, self.model, "list")
        pywatch.wx.ItemContainerItemWatcher(self.choice, self.model, "list")
        pywatch.wx.ItemContainerItemWatcher(self.combo_box, self.model, "list")

    # Virtual event handlers, overide them in your derived class
    def on_add(self, event):
        if self.model["text"]:
            self.model["list"].append(self.model["text"])
            self.model["text"] = ""
        event.Skip()


if __name__ == "__main__":
    app = wx.App()
    top = MyFrame(None)
    top.Show()
    app.MainLoop()
