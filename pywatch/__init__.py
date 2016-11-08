import logging
import traceback


class Watcher:
    def __init__(self, watch_object, item):
        self.watch_object = watch_object
        self.item = item
        self.listeners = []

    def bind(self, callback):
        self.listeners.append(callback)

    def notify(self):
        for listener in self.listeners:
            try:
                listener()
            except Exception as e:
                logging.error(traceback.format_exc())

    def get_value(self):
        return self.watch_object[self.item]

    def set_value(self, value):
        self.watch_object[self.item] = value


class WatchableDict(dict):
    def __init__(self, seq=None, **kwargs):
        self.watchers = {}
        dict.__init__(self)

    def __setitem__(self, item, new_value):
        new_b = item in self
        old_value = self[item] if item in self else None
        dict.__setitem__(self, item, new_value)
        if new_b:
            if old_value != new_value:
                self.watchers[item].notify()
        else:
            self.watchers[item] = Watcher(self, item)

    def get_watcher(self, name):
        if name in self.watchers:
            return self.watchers[name]
        return None


class PropertyWatcher:
    def __init__(self, widget, watcher):
        self.widget = widget
        self.watcher = watcher
        watcher.bind(self.callback)

    def callback(self):
        pass
