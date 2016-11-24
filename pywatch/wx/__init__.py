import wx

from .. import Watcher, MultipleWatcher, Changer



def call_after(func):
    def my_call_after(*args, **kwargs):
        wx.CallAfter(func, *args, **kwargs)

    return my_call_after


class EnableWatcher(Watcher):
    def __init__(self, widget, watchable, watcher):
        Watcher.__init__(self, widget, watchable, watcher)
        self.widget.Enable(self.get_value())

    def callback(self):
        self.widget.Enable(self.get_value())


class LabelWatcher(MultipleWatcher):
    def __init__(self, widget, watchable, *watchers):
        MultipleWatcher.__init__(self, widget, watchable, *watchers)
        self.format = widget.GetLabel()
        self.callback()

    @call_after
    def callback(self):
        t = self.get_values()
        self.widget.SetLabel(self.format.format(*t))
        self.widget.GetParent().Layout()


class LabelMarkupWatcher(MultipleWatcher):
    def __init__(self, widget, watchable, *watchers):
        MultipleWatcher.__init__(self, widget, watchable, *watchers)
        self.format = widget.GetLabel()
        self.callback()

    @call_after
    def callback(self):
        t = self.get_values()
        self.widget.SetLabelMarkup(self.format.format(*t))
        self.widget.GetParent().Layout()


class ValueWatcher(Watcher):
    def __init__(self, widget, watchable, watcher):
        Watcher.__init__(self, widget, watchable, watcher)
        self.widget.SetValue(self.get_value())

    @call_after
    def callback(self):
        if self.widget.GetValue() != self.get_value():
            self.widget.SetValue(self.get_value())


value_events = {
    wx.SpinCtrl: wx.EVT_SPINCTRL,
    wx.Slider: wx.EVT_SLIDER,
    wx.CheckBox: wx.EVT_CHECKBOX,
    wx.ToggleButton: wx.EVT_TOGGLEBUTTON,
    wx.TextCtrl: wx.EVT_TEXT
}


class ValueChanger(Changer):
    def __init__(self, widget, watchable, watcher):
        event = [value_events[widget_class] for widget_class in value_events if isinstance(widget, widget_class)]
        if not event:
            raise Exception('Widget type is not recognised')
        Changer.__init__(self, widget, watchable, watcher)
        self.widget.SetValue(self.get_value())
        widget.Bind(event[0], self.on_change)

    def on_change(self, event):
        self.set_value(self.widget.GetValue())
        event.Skip()

    @call_after
    def callback(self):
        current_value = self.widget.GetValue()
        new_value = self.get_value()
        if self.widget.GetValue() != self.get_value():
            self.widget.SetValue(self.get_value())


selection_events = {
    wx.ComboBox: wx.EVT_COMBOBOX,
    wx.Choice: wx.EVT_CHOICE,
    wx.ListBox: wx.EVT_LISTBOX,
    wx.RadioBox: wx.EVT_RADIOBOX
}


class SelectionChanger(Changer):
    def __init__(self, widget, watchable, watcher):
        event = [selection_events[widget_class] for widget_class in selection_events if
                 isinstance(widget, widget_class)]
        if not event:
            raise Exception('Widget type is not recognised')
        Changer.__init__(self, widget, watchable, watcher)
        self.widget.SetSelection(self.get_value())
        widget.Bind(event[0], self.on_change)

    @call_after
    def callback(self):
        if self.widget.GetSelection() != self.get_value():
            self.widget.SetSelection(self.get_value())

    def on_change(self, event):
        self.set_value(self.widget.GetSelection())
        event.Skip()


class ItemContainerItemWatcher(Watcher):
    def __init__(self, item_container, watchable, watcher, format_string='{0}'):
        Watcher.__init__(self, item_container, watchable, watcher)
        self.format_string = format_string
        for item in self.get_value():
            index = self.widget.Append(format_string.format(item), item)

    @call_after
    def callback(self):
        data = None
        if self.widget.GetSelection() != -1:
            data = self.widget.GetClientData(self.widget.GetSelection())
        self.widget.Freeze()
        self.widget.Clear()
        for item in self.get_value():
            index = self.widget.Append(self.format_string.format(item), item)
            if data is not None and item is data:
                self.widget.SetSelection(index)
        self.widget.Thaw()
