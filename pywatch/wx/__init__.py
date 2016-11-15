import wx

from .. import Watcher, MultipleWatcher


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


class SelectionChangeWatcher(Watcher):
    def __init__(self, widget, watchable, watcher, event):
        Watcher.__init__(self, widget, watchable, watcher)
        self.widget.SetSelection(self.get_value(self.widget.GetSelection()))
        widget.Bind(event, self.on_change)

    @call_after
    def callback(self):
        if self.widget.GetSelection() != self.get_value():
            self.widget.SetSelection(self.get_value())

    def on_change(self, event):
        self.set_value(self.widget.GetSelection())
        event.Skip()


class ListBoxWatcher(SelectionChangeWatcher):
    def __init__(self, list_box, watchable, watcher):
        SelectionChangeWatcher.__init__(self, list_box, watchable, watcher, wx.EVT_LISTBOX)


class RadioBoxWatcher(SelectionChangeWatcher):
    def __init__(self, radio_box, watchable, watcher):
        SelectionChangeWatcher.__init__(self, radio_box, watchable, watcher, wx.EVT_RADIOBOX)


class ChoiceWatcher(SelectionChangeWatcher):
    def __init__(self, radio_box, watchable, watcher):
        SelectionChangeWatcher.__init__(self, radio_box, watchable, watcher, wx.EVT_CHOICE)


class ComboBoxWatcher(SelectionChangeWatcher):
    def __init__(self, radio_box, watchable, watcher):
        SelectionChangeWatcher.__init__(self, radio_box, watchable, watcher, wx.EVT_COMBOBOX)


class SpinCtrlWatcher(ValueChangeWatcher):
    def __init__(self, spin_ctrl, watchable, watcher):
        ValueChangeWatcher.__init__(self, spin_ctrl, watchable, watcher, wx.EVT_SPINCTRL)


class SliderWatcher(ValueChangeWatcher):
    def __init__(self, spin_ctrl, watchable, watcher):
        ValueChangeWatcher.__init__(self, spin_ctrl, watchable, watcher, wx.EVT_SCROLL)


class CheckBoxWatcher(ValueChangeWatcher):
    def __init__(self, check_box, watchable, watcher):
        ValueChangeWatcher.__init__(self, check_box, watchable, watcher, wx.EVT_CHECKBOX)


class ToggleButtonWatcher(ValueChangeWatcher):
    def __init__(self, toggle_btn, watchable, watcher):
        ValueChangeWatcher.__init__(self, toggle_btn, watchable, watcher, wx.EVT_TOGGLEBUTTON)


class TextCtrlWatcher(ValueChangeWatcher):
    def __init__(self, text_ctrl, watchable, watcher):
        ValueChangeWatcher.__init__(self, text_ctrl, watchable, watcher, wx.EVT_TEXT)


class ItemContainerItemWatcher(Watcher):
    def __init__(self, item_container, watchable, watcher):
        Watcher.__init__(self, item_container, watchable, watcher)
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
