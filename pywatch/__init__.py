import logging
import traceback


class WatchableDict(dict):
    def __init__(self, *args, **kwargs):
        self.watchers = {}
        dict.__init__(self, *args, **kwargs)

    def __setitem__(self, item, value):
        if item in self:
            changed = self[item] != value
        else:
            changed = True
        super(WatchableDict, self).__setitem__(item, value)
        if item in self.watchers:
            if changed:
                for watcher in self.watchers[item]:
                    try:
                        watcher()
                    except Exception as e:
                        logging.error(traceback.format_exc())

    def bind(self, callback, name):
        if name in self.watchers:
            self.watchers[name].append(callback)
        else:
            self.watchers[name] = [callback]


class Watcher:
    def __init__(self, widget, watchable, watch):
        self.widget = widget
        self.watchable = watchable
        self.watcher = watch
        watchable.bind(self.callback, watch)

    def get_value(self):
        return self.watchable[self.watcher]

    def set_value(self, value):
        self.watchable[self.watcher] = value

    def callback(self):
        pass


class MultipleWatcher:
    def __init__(self, widget, watchable, watchers):
        self.widget = widget
        self.watchable = watchable
        self.watchers = watchers
        for watch in watchers:
            watchable.bind(self.callback, watch)

    def callback(self):
        pass
