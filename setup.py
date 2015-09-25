#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of tornado-eventbus.
# https://github.com/thumby/tornado-eventbus

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

from setuptools import setup, find_packages
from tornado_eventbus import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    #'ipdb',
    #'coveralls',
    #'sphinx',
]

setup(
    name='tornado-eventbus',
    version=__version__,
    description='tornado-eventbus is an asynchronous event bus for tornado applications.',
    long_description='''
tornado-eventbus is an asynchronous event bus for tornado applications.
''',
    keywords='tornado python asynchronous async event bus',
    author='Bernardo Heynemann',
    author_email='heynemann@gmail.com',
    url='https://github.com/thumby/tornado-eventbus',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'tornado>=4.2.0,<5.0.0',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'tornado-eventbus=tornado_eventbus.cli:main',
        ],
    },
)
