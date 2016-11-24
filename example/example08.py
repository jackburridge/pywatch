import wx

import pywatch.wx
from pywatch import WatchableDict


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Person Editor", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.model = WatchableDict({
            "people": [
                {
                    "name": "Bob",
                    "age": 40
                },
                {
                    "name": "Jack",
                    "age": 20
                },
            ],
            "selection": 0
        })

        sizer = wx.BoxSizer(wx.VERTICAL)

        gb_sizer = wx.GridBagSizer(5, 5)
        gb_sizer.SetFlexibleDirection(wx.BOTH)
        gb_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.person_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [], 0)
        self.person_choice.SetSelection(0)
        gb_sizer.Add(self.person_choice, wx.GBPosition(0, 0), wx.GBSpan(1, 2), wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        pywatch.wx.ItemContainerItemWatcher(self.person_choice, self.model, "people",
                                            format_string="{0[name]} - {0[age]}")
        pywatch.wx.SelectionChanger(self.person_choice, self.model, "selection")

        self.name_static_text = wx.StaticText(self, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0)
        self.name_static_text.Wrap(-1)
        gb_sizer.Add(self.name_static_text, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALIGN_CENTER_VERTICAL, 0)

        self.name_text_ctrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gb_sizer.Add(self.name_text_ctrl, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)

        def get_name():
            return self.model["people"][self.model["selection"]]["name"]

        def set_name(value):
            self.model["people"][self.model["selection"]]["name"] = value

        pywatch.wx.ValueChanger(self.name_text_ctrl, self.model, ("person", "selection", set_name, get_name))

        self.age_static_text = wx.StaticText(self, wx.ID_ANY, u"Age", wx.DefaultPosition, wx.DefaultSize, 0)
        self.age_static_text.Wrap(-1)
        gb_sizer.Add(self.age_static_text, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALIGN_CENTER_VERTICAL, 0)

        self.age_spin_ctrl = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                         wx.SP_ARROW_KEYS, 0, 100, 0)
        gb_sizer.Add(self.age_spin_ctrl, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)

        def get_age():
            return self.model["people"][self.model["selection"]]["age"]

        def set_age(value):
            self.model["people"][self.model["selection"]]["age"] = value

        pywatch.wx.ValueChanger(self.age_spin_ctrl, self.model, ("person", "selection", set_age, get_age))

        gb_sizer.AddGrowableCol(1)

        sizer.Add(gb_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()

        self.Centre(wx.BOTH)


if __name__ == "__main__":
    app = wx.App()
    top = MyFrame(None)
    top.Show()
    app.MainLoop()
