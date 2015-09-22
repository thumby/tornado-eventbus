#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of tornado-eventbus.
# https://github.com/thumby/tornado-eventbus

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

from preggy import expect

from tests.base import TestCase


class TornadoEventBusTestCase(TestCase):
    def test_can_subscribe_to_event(self):
        response = self.fetch('/')
        expect(response.code).to_equal(200)
        expect(self.result).to_include('before-hello')
        expect(self.result).to_include('after-hello')
