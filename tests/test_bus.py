#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of tornado-eventbus.
# https://github.com/thumby/tornado-eventbus

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

from preggy import expect

from tornado_eventbus.bus import EventData
from tests.base import TestCase


class TornadoEventBusTestCase(TestCase):
    def test_can_subscribe_to_event(self):
        response = self.fetch('/')
        expect(response.code).to_equal(200)
        expect(self.result).to_include('before-hello')
        expect(self.result).to_include('after-hello')

        expect(self.result['before-hello']).to_be_instance_of(EventData)
        expect(self.order).to_equal([
            ('before-hello', 'outside'),
            ('before-hello', 'main-handler'),
            ('after-hello', 'on_after_hello'),
        ])

    def test_can_subscribe_to_events_in_parallel(self):
        response = self.fetch('/parallel')
        expect(response.code).to_equal(200)
        expect(self.result).to_include('before-hello')
        expect(self.result).to_include('after-hello')

        expect(self.result['before-hello']).to_be_instance_of(EventData)
        expect(self.order).to_equal([
            ('before-hello', 'main-handler'),
            ('after-hello', 'on_after_hello'),
            ('before-hello', 'outside'),
        ])
