import logging
import traceback


class Watchable:
    def __init__(self, parent):
        self.parent = parent
        self.watchers = {}

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
        if name in self.watchers:
            self.watchers[name].append(callback)
        else:
            self.watchers[name] = [callback]


class WatchableList(list, Watchable):
    def __init__(self, iterable=None, parent=None):
        Watchable.__init__(self, parent)
        list.__init__(self, iterable)

    def __setitem__(self, key, value):
        value = self._set_watchable(value)
        list.__setitem__(self, key, value)
        self._notify_parent()

    def append(self, p_object):
        value = self._set_watchable(p_object)
        list.append(self, p_object)
        self._notify_parent()


class WatchableDict(dict, Watchable):
    def __init__(self, parent=None, **kwargs):
        Watchable.__init__(self, parent)
        dict.__init__(self, **kwargs)

    def child_change(self, value):
        if self.parent:
            self.parent.child_change()
        for key, item in self.iteritems():
            if item == value:
                self._notify_watchers(key)
                break

    def __setitem__(self, key, value):
        value = self._set_watchable(value)
        dict.__setitem__(self, key, value)
        self._notify_watchers(key)


def get_watchers(watcher):
    if isinstance(watcher, basestring):
        return [watcher]
    else:
        return watcher[:-1]


def get_watcher_value(watchable, watcher):
    if isinstance(watcher, basestring):
        return watchable[watcher]
    else:
        t = tuple(watchable[w] for w in watcher[:-1])
        return watcher[-1](*t)


class Watcher:
    def __init__(self, widget, watchable, watcher):
        self.widget = widget
        self.watchable = watchable
        self.watcher = watcher
        for w in set(get_watchers(watcher)):
            watchable.bind(self.callback, w)

    def get_value(self, value=None):
        if self.watcher not in self.watchable:
            self.watchable[self.watcher] = value
        return get_watcher_value(self.watchable, self.watcher)

    def set_value(self, value):
        self.watchable[self.watcher] = value

    def callback(self):
        pass


class MultipleWatcher:
    def __init__(self, widget, watchable, *watchers):
        self.widget = widget
        self.watchable = watchable
        self.watchers = watchers
        watchers_all = []
        for w in watchers:
            watchers_all += get_watchers(w)
        for w in set(watchers_all):
            watchable.bind(self.callback, w)

    def get_values(self):
        return tuple(get_watcher_value(self.watchable, watcher) for watcher in self.watchers)

    def callback(self):
        pass
