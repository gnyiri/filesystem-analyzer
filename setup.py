# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='filesystem-analyzer',
    version='1.0',
    description='File System analyzer',
    long_description=readme,
    author='Gergely Nyiri',
    author_email='gergely.nyiri@gmail.com',
    url='https://gitlab.com/gergely.nyiri/filesystem-analyzer',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
