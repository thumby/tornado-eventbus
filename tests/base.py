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
order = []


@bus.subscribe("before-hello", key="outside")
def on_before_hello_2(sender, ev):
    global result, order
    yield ev.wait_for("main-handler")
    yield ev.wait_for("invalid-handler")
    order.append(('before-hello', 'outside'))
    result["before-hello-outside"] = ev


class MainHandler(web.RequestHandler, bus.Publisher):

    @staticmethod
    @bus.subscribe("before-hello", key="main-handler")
    def on_before_hello(sender, ev):
        global result
        order.append(('before-hello', 'main-handler'))
        result["before-hello"] = ev

    @staticmethod
    @bus.subscribe("after-hello")
    def on_after_hello(sender, ev):
        global result
        order.append(('after-hello', 'on_after_hello'))
        result["after-hello"] = ev

    @gen.coroutine
    def get(self):
        yield self.publish("before-hello", hello="world")
        self.write("Hello, world")
        yield self.publish("after-hello", hello="world")


class ParallelHandler(web.RequestHandler, bus.Publisher):

    @gen.coroutine
    def get(self):
        yield self.publish("before-hello", parallel=True, hello="world")
        self.write("Hello, world")
        yield self.publish("after-hello", parallel=True, hello="world")


class TestCase(AsyncHTTPTestCase):
    @property
    def result(self):
        global result
        return result

    @property
    def order(self):
        global order
        return order

    def setUp(self, *args, **kw):
        global result, order

        super(TestCase, self).setUp(*args, **kw)

        result = {}
        order = []

    def get_app(self):
        app = web.Application(
            [
                ('/', MainHandler),
                ('/parallel', ParallelHandler),
            ]
        )

        bus.initialize(app)

        return app
