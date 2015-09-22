#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of tornado-eventbus.
# https://github.com/thumby/tornado-eventbus

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>


from collections import defaultdict

from tornado.gen import coroutine


class EventData(object):
    def __init__(self, **kw):
        for key in kw:
            setattr(self, key, kw[key])


class EventBus(object):
    def __init__(self):
        self.subscriptions = defaultdict(list)
        self.Publisher = publisher_mixin(bus=self)

    def initialize(self, app):
        self.tornado_app = app

    def subscribe(self, key):
        def tags_decorator(func):
            self.subscriptions[key].append(coroutine(func))
            return func
        return tags_decorator

    @coroutine
    def publish(self, key, instance=None, **kw):
        if key not in self.subscriptions or not self.subscriptions[key]:
            return

        yield [
            method(EventData(**kw))
            if instance is None
            else method(instance, EventData(**kw))
            for method in self.subscriptions[key]
        ]


def publisher_mixin(bus):
    class Publisher(object):
        @coroutine
        def publish(self, key, **kw):
            yield bus.publish(key, instance=bus, **kw)

    return Publisher
