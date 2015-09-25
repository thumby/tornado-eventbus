#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of tornado-eventbus.
# https://github.com/thumby/tornado-eventbus

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>


from collections import defaultdict

try:
    from tornado.gen import coroutine
    from tornado.locks import Condition
except ImportError:
    print("Error importing tornado. Probably setup.py installing tornado_eventbus...")

    def coroutine(func):
        def handle(*args, **kw):
            func()
        return handle


class EventData(object):
    def __init__(self, bus, event, parallel, **kw):
        self.bus = bus
        self.event = event
        self.parallel = parallel
        for key in kw:
            setattr(self, key, kw[key])

    @coroutine
    def wait_for(self, key):
        if not self.parallel:
            return
        if self.event not in self.bus.conditions or key not in self.bus.conditions[self.event]:
            return
        condition = self.bus.conditions[self.event][key]
        yield condition.wait()


class EventBus(object):
    def __init__(self):
        self.subscriptions = defaultdict(list)
        self.conditions = defaultdict(dict)
        self.Publisher = publisher_mixin(bus=self)

    def initialize(self, app):
        self.tornado_app = app

    def subscribe(self, event, key=None):
        def tags_decorator(func):
            event_key = key
            if event_key is None:
                event_key = func.__name__

            if event_key in self.conditions[event]:
                raise RuntimeError("Callback key %s for event %s is repeated." % (key, event))

            self.subscriptions[event].append({
                'key': event_key,
                'func': coroutine(func),
            })
            self.conditions[event][event_key] = Condition()

            return func
        return tags_decorator

    def notify_finished(self, event, key):
        if event not in self.conditions or key not in self.conditions[event]:
            return

        condition = self.conditions[event][key]
        condition.notify()

    @coroutine
    def publish(self, event, sender, parallel=False, **kw):
        if event not in self.subscriptions or not self.subscriptions[event]:
            return

        if not parallel:
            for callback_data in self.subscriptions[event]:
                yield callback_data['func'](sender, EventData(self, event, parallel, **kw))
        else:
            yield [
                self.run_event(event, callback_data['key'], sender, callback_data['func'], parallel, **kw)
                for callback_data in self.subscriptions[event]
            ]

    @coroutine
    def run_event(self, event, key, sender, func, parallel, **kw):
        func(sender, EventData(self, event, parallel, **kw))
        self.notify_finished(event, key)


def publisher_mixin(bus):
    class Publisher(object):
        @coroutine
        def publish(self, key, **kw):
            yield bus.publish(key, sender=self, **kw)

    return Publisher
