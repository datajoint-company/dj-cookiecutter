#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path
import sys

## Description
description = '' # TODO - description
keywords = '' # TODO - modalities
with open(path.join(here, 'README.md'), 'r') as f:
    long_description = f.read()

here = path.abspath(path.dirname(__file__))

## Get version
pkg_name = 'workflow'
with open(path.join(here, pkg_name, 'version.py')) as f:
    exec(f.read())

## Get requirement list
with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().split()

## Min python version 
min_py_version = (3, 6)
if sys.version_info <  min_py_version:
    sys.exit('DataJoint is only supported for Python {}.{} or higher'.format(*min_py_version))

{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'GNU Lesser General Public License v3.0': 'OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)'
} %}

setup(
    name='{{ cookiecutter.project_slug }}',
    version=__version__,
    description=description,
    long_description=long_description,
    author='{{ cookiecutter.author_name.replace('\"', '\\\"') }}',
    author_email='{{ cookiecutter.author_email }}',
{%- if cookiecutter.license in license_classifiers %}
    license="{{ cookiecutter.license }}",
{%- endif %}
    url='https://www.datajoint.com/solutions',
    keywords='datajoint sciops workflow {}'.format(keywords),
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    install_requires=requirements,
    python_requires='~={}.{}'.format(*min_py_version),
    entry_points={
        'console_scripts': ['run_workflow=workflow.process:cli'],
    }
)