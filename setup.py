#!/usr/bin/env python

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
  name = 'gcsms',
  version = '2.0',
  packages = ['gcsms'],
  entry_points = {
    'console_scripts': [
      'gcsms = gcsms:main'
    ]
  },

  author = 'Mansour Behabadi',
  author_email = 'mansour@oxplot.com',
  description = 'Send SMS for free using Google Calendar',
  long_description =
    'See https://github.com/oxplot/gcsms/blob/master/README.md',
  license = 'GPLv3',
  url = 'https://github.com/oxplot/gcsms'
)
