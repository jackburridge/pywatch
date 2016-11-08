import wx

from .. import PropertyWatcher


class EnableWatcher(PropertyWatcher):
    def __init__(self, widget, watcher):
        PropertyWatcher.__init__(self, widget, watcher)
        self.widget.Enable(watcher.get_value())

    def callback(self):
        self.widget.Enable(self.watcher.get_value())


class LabelWatcher:
    def __init__(self, widget, watchers, format="%s"):
        self.widget = widget
        self.format = format
        self.watchers = watchers
        for watcher in watchers:
            watcher.bind(self.callback)

        self.__set_label()

    def __set_label(self):
        self.widget.SetLabel(self.format % tuple(watcher.get_value() for watcher in self.watchers))

    def callback(self):
        self.__set_label()
        self.widget.GetParent().Layout()


class ValueWatcher(PropertyWatcher):
    def __init__(self, widget, watcher):
        PropertyWatcher.__init__(self, widget, watcher)
        self.widget.SetValue(watcher.get_value())

    def callback(self):
        if wx.Window.FindFocus() != self.widget:
            self.widget.SetValue(self.watcher.get_value())


class ValueChangeWatcher(ValueWatcher):
    def __init__(self, widget, watcher, event):
        ValueWatcher.__init__(self, widget, watcher)
        widget.Bind(event, self.on_change)

    def on_change(self, event):
        self.watcher.set_value(self.widget.GetValue())
        event.Skip()


class SpinCtrlWatcher(ValueChangeWatcher):
    def __init__(self, spin_ctrl, watcher):
        ValueChangeWatcher.__init__(self, spin_ctrl, watcher, wx.EVT_SPINCTRL)


class SliderWatcher(ValueChangeWatcher):
    def __init__(self, spin_ctrl, watcher):
        ValueChangeWatcher.__init__(self, spin_ctrl, watcher, wx.EVT_SCROLL)


class GaugeWatcher(ValueWatcher):
    def __init__(self, gauge, watcher):
        ValueWatcher.__init__(self, gauge, watcher)


class CheckBoxWatcher(ValueChangeWatcher):
    def __init__(self, check_box, watcher):
        ValueChangeWatcher.__init__(self, check_box, watcher, wx.EVT_CHECKBOX)


class ToggleButtonWatcher(ValueChangeWatcher):
    def __init__(self, toggle_btn, watcher):
        ValueChangeWatcher.__init__(self, toggle_btn, watcher, wx.EVT_TOGGLEBUTTON)


class TextCtrlWatcher(ValueChangeWatcher):
    def __init__(self, toggle_btn, watcher):
        ValueChangeWatcher.__init__(self, toggle_btn, watcher, wx.EVT_TEXT)
