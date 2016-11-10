import wx

from .. import Watcher, MultipleWatcher


class EnableWatcher(Watcher):
    def __init__(self, widget, watchable, watcher):
        Watcher.__init__(self, widget, watchable, watcher)
        self.widget.Enable(self.get_value())

    def callback(self):
        self.widget.Enable(self.get_value())


class LabelWatcher(MultipleWatcher):
    def __init__(self, widget, watchable, watchers, format="{0}"):
        MultipleWatcher.__init__(self, widget, watchable, watchers)
        self.format = format

        self.__set_label()

    def __set_label(self):
        t = self.get_values()
        self.widget.SetLabel(self.format.format(*t))

    def callback(self):
        self.__set_label()
        self.widget.GetParent().Layout()


class LabelMarkupWatcher(MultipleWatcher):
    def __init__(self, widget, watchable, watchers, format="{0}"):
        MultipleWatcher.__init__(self, widget, watchable, watchers)
        self.format = format

        self.__set_label()

    def __set_label(self):
        t = self.get_values()
        self.widget.SetLabelMarkup(self.format.format(*t))

    def callback(self):
        self.__set_label()
        self.widget.GetParent().Layout()


class ValueWatcher(Watcher):
    def __init__(self, widget, watchable, watcher):
        Watcher.__init__(self, widget, watchable, watcher)
        self.widget.SetValue(self.get_value(self.widget.GetValue()))

    def callback(self):
        if self.widget.GetValue() != self.get_value():
            self.widget.SetValue(self.get_value())


class ValueChangeWatcher(ValueWatcher):
    def __init__(self, widget, watchable, watcher, event):
        ValueWatcher.__init__(self, widget, watchable, watcher)
        widget.Bind(event, self.on_change)

    def on_change(self, event):
        self.set_value(self.widget.GetValue())
        event.Skip()


class SpinCtrlWatcher(ValueChangeWatcher):
    def __init__(self, spin_ctrl, watchable, watcher):
        ValueChangeWatcher.__init__(self, spin_ctrl, watchable, watcher, wx.EVT_SPINCTRL)


class SliderWatcher(ValueChangeWatcher):
    def __init__(self, spin_ctrl, watchable, watcher):
        ValueChangeWatcher.__init__(self, spin_ctrl, watchable, watcher, wx.EVT_SCROLL)


class GaugeWatcher(ValueWatcher):
    def __init__(self, gauge, watchable, watcher):
        ValueWatcher.__init__(self, gauge, watchable, watcher)


class CheckBoxWatcher(ValueChangeWatcher):
    def __init__(self, check_box, watchable, watcher):
        ValueChangeWatcher.__init__(self, check_box, watchable, watcher, wx.EVT_CHECKBOX)


class ToggleButtonWatcher(ValueChangeWatcher):
    def __init__(self, toggle_btn, watchable, watcher):
        ValueChangeWatcher.__init__(self, toggle_btn, watchable, watcher, wx.EVT_TOGGLEBUTTON)


class TextCtrlWatcher(ValueChangeWatcher):
    def __init__(self, toggle_btn, watchable, watcher):
        ValueChangeWatcher.__init__(self, toggle_btn, watchable, watcher, wx.EVT_TEXT)


class ListBoxItemWatcher(Watcher):
    def __init__(self, listbox, watchable, watcher):
        Watcher.__init__(self, listbox, watchable, watcher)
        self.__set_items()

    def __set_items(self):
        t = tuple("{0}".format(item) for item in self.watchable[self.watcher])
        self.widget.SetItems(t)

    def callback(self):
        self.__set_items()
