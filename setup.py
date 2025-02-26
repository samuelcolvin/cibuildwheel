#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, io

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

this_directory = os.path.dirname(__file__)
with io.open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cibuildwheel',
    version='1.1.0',
    install_requires=['bashlex!=0.13'],
    description="Build Python wheels on CI with minimal configuration.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Joe Rickerby",
    author_email='joerick@mac.com',
    url='https://github.com/joerick/cibuildwheel',
    packages=['cibuildwheel',],
    license="BSD",
    zip_safe=False,
    package_data={
        'cibuildwheel': ['resources/*'],
    },
    # Supported python versions
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    keywords='ci wheel packaging pypi travis appveyor macos linux windows',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Build Tools',
    ],
    entry_points={
        'console_scripts': [
            'cibuildwheel = cibuildwheel.__main__:main',
        ],
    },
)
