#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of tornado-eventbus.
# https://github.com/thumby/tornado-eventbus

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

from tornado import gen, web
from tornado.testing import AsyncHTTPTestCase

from tornado_eventbus import EventBus

bus = EventBus()


result = {}


class MainHandler(web.RequestHandler, bus.Publisher):

    @bus.subscribe("before-hello")
    def on_before_hello(self, ev):
        global result
        result["before-hello"] = ev

    @bus.subscribe("after-hello")
    def on_after_hello(self, ev):
        global result
        result["after-hello"] = ev

    @gen.coroutine
    def get(self):
        yield self.publish("before-hello", hello="world")
        self.write("Hello, world")
        yield self.publish("after-hello", hello="world")


class TestCase(AsyncHTTPTestCase):
    @property
    def result(self):
        global result
        return result

    def get_app(self):
        app = web.Application(
            [
                ('/', MainHandler)
            ]
        )

        bus.initialize(app)

        return app
