import logging
import traceback
from collections import defaultdict


class Watchable:
    def __init__(self, parent):
        self.parent = parent
        self.watchers = defaultdict(list)

    def _set_watchable(self, value):
        types = {dict: WatchableDict,
                 list: WatchableList}
        for type in types:
            if isinstance(value, type):
                value = types[type](value, parent=self)
                break
        return value

    def child_change(self, value):
        if self.parent:
            self.parent.child_change(self)

    def _notify_parent(self):
        if self.parent:
            self.parent.child_change(self)

    def _notify_watchers(self, key):
        self._notify_parent()
        if key in self.watchers:
            for watcher in self.watchers[key]:
                try:
                    watcher()
                except Exception as e:
                    logging.error(traceback.format_exc())

    def bind(self, callback, name):
        self.watchers[name].append(callback)


class WatchableList(list, Watchable):
    def __init__(self, iterable=None, parent=None):
        Watchable.__init__(self, parent)
        watchable_iterable = [self._set_watchable(item) for item in iterable]
        list.__init__(self, watchable_iterable)

    def __setitem__(self, key, value):
        value = self._set_watchable(value)
        list.__setitem__(self, key, value)
        self._notify_parent()

    def append(self, p_object):
        value = self._set_watchable(p_object)
        list.append(self, value)
        self._notify_parent()

    def pop(self, index=None):
        list.pop(self, index)
        self._notify_parent()


class WatchableDict(dict, Watchable):
    def __init__(self, seq=None, **kwargs):
        parent = kwargs.pop('parent', None)
        Watchable.__init__(self, parent)
        iterable_seq = {}
        if seq:
            for key, value in dict(seq).iteritems():
                iterable_seq[key] = self._set_watchable(value)
        dict.__init__(self, iterable_seq, **kwargs)

    def child_change(self, value):
        if self.parent:
            self.parent.child_change(self)
        for key, item in self.iteritems():
            if item == value:
                self._notify_watchers(key)
                break

    def __setitem__(self, key, value):
        value = self._set_watchable(value)
        dict.__setitem__(self, key, value)
        self._notify_watchers(key)

    def update(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError("update expected at most 1 arguments, got %d" % len(args))
        other = dict(*args, **kwargs)
        for key in other:
            self[key] = other[key]


class Observer:
    def __init__(self, widget, watchable, watch_values, getter):
        self.widget = widget
        self.watchable = watchable
        self.getter = getter
        for watch_value in set(watch_values):
            watchable.bind(self.callback, watch_value)

    def callback(self):
        raise NotImplementedError()


class Watcher(Observer):
    def __init__(self, widget, watchable, watcher):
        if isinstance(watcher, basestring):
            watch_values = [watcher]
            getter = lambda: watchable[watcher]
        else:
            watch_values = watcher[:-1]
            getter = watcher[-1]
        Observer.__init__(self, widget, watchable, watch_values, getter)

    def get_value(self):
        return self.getter()


class MultipleWatcher(Observer):
    def __init__(self, widget, watchable, *watchers):
        watch_values = set()
        getters = []
        for watcher in watchers:
            if isinstance(watcher, basestring):
                watch_values.add(watcher)
                getters.append(lambda: watchable[watcher])
            else:
                watch_values.update(watcher[:-1])
                getters.append(watcher[-1])
        Observer.__init__(self, widget, watchable, watch_values, getters)

    def get_values(self):
        return tuple(get() for get in self.getter)

    def callback(self):
        raise NotImplementedError()


class Changer(Watcher):
    def __init__(self, widget, watchable, watcher):
        if isinstance(watcher, basestring):
            watch_values = [watcher]
            getter = lambda: watchable[watcher]
            self.setter = lambda value: watchable.update({watcher: value})
        else:
            watch_values = watcher[:-2]
            getter = watcher[-1]
            self.setter = watcher[-2]
        Observer.__init__(self, widget, watchable, watch_values, getter)

    def set_value(self, value):
        if self.get_value() != value:
            self.setter(value)
