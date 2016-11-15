import wx

from .. import Watcher, MultipleWatcher


def call_after(func):
    def mycallafter(*args, **kws):
        wx.CallAfter(func, *args, **kws)

    return mycallafter


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

    @call_after
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


SpinCtrlWatcher = ValueChangeWatcher

SliderWatcher = ValueChangeWatcher

GaugeWatcher = ValueWatcher

CheckBoxWatcher = ValueChangeWatcher

ToggleButtonWatcher = ValueChangeWatcher

TextCtrlWatcher = ValueChangeWatcher


class ItemContainerItemWatcher(Watcher):
    def __init__(self, listbox, watchable, watcher):
        Watcher.__init__(self, listbox, watchable, watcher)
        self.callback()

    @call_after
    def callback(self):
        data = None
        if self.widget.GetSelection() != -1:
            data = self.widget.GetClientData(self.widget.GetSelection())
        self.widget.Freeze()
        self.widget.Clear()
        for item in self.watchable[self.watcher]:
            index = self.widget.Append("{0}".format(item), item)
            if data is not None and item is data:
                self.widget.SetSelection(index)
        self.widget.Thaw()
