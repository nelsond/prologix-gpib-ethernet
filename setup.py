# -*- coding: utf-8 -*-
from setuptools import setup
import os
from plx_gpib_ethernet import __version__

current_path = os.path.dirname(os.path.abspath(__file__))

# Get the long description from the README file
with open(os.path.join(current_path, 'README.md')) as f:
    long_description = f.read()

setup(
    name='prologix-gpib-ethernet',

    version=__version__,

    description='Simple wrapper for the Prologix GPIB-to-Ethernet adapter.',
    long_description=long_description,

    url='https://github.com/nelsond/prologix-gpib-ethernet',

    author='Nelson Darkwah Oppong',
    author_email='n@darkwahoppong.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Stable',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='gpib prologix',

    packages=['plx_gpib_ethernet'],

    install_requires=[],
)
