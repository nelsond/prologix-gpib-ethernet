# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open('README.rst').read()
except IOError:
    long_description = ''

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    required = f.read().splitlines()

setup(
    name='prologix-gpib-ethernet',

    use_scm_version=True,
    setup_requires=['setuptools_scm'],

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

    install_requires=required,
)
