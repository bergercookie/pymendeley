#!/usr/bin/env python

try:
    from setuptools import setup
except:
    from distutils.core import setup

PKG_NAME = "lmendeley"

setup(name='pymendeley',
      packages=[PKG_NAME],
      install_requires=(
          "configparser",
      ),
      version='0.1.1',
      description='Python library for accessing the local Mendeley sqlite3 database.',
      author='James Brotchie',
      author_email='brotchie@gmail.com',
      maintainer='Nikos Koukis',
      maintainer_email='nickkouk@gmail.com',
      url='https://github.com/bergercookie/pymendeley',
      download_url='https://github.org/bergercookie/pymendeley',
      platforms="Linux",
      )
