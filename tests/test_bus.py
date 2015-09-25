#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of tornado-eventbus.
# https://github.com/thumby/tornado-eventbus

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

from preggy import expect

from tornado_eventbus.bus import EventData, EventBus
from tests.base import TestCase, bus


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

    def test_subscribing_twice_fails(self):
        @bus.subscribe("some-event", key="1")
        def test(sender, ev):
            pass

        try:
            @bus.subscribe("some-event", key="1")
            def test2(sender, ev):
                pass
        except RuntimeError as ex:
            expect(ex).to_be_an_error()
            expect(ex).to_have_an_error_message_of("Callback key 1 for event some-event is repeated.")
        else:
            assert False, "should not have gotten this far"

    def test_can_notify_event_without_callbacks(self):
        bus = EventBus()
        bus.notify_finished("some", "event")

        expect(bus.conditions).to_be_empty()

    def test_can_publish_event_without_listeners(self):
        bus = EventBus()
        bus.publish("fake-event", self, argument="123")

        expect(bus.subscriptions).to_be_empty()
