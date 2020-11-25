# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='bank',
    version='0.1.0',
    description='Banking System to exercise Python OOP',
    author='Colathur Vijayan',
    author_email='colathurv@yahoo.com',
    url='https://github.com/colathurv/banking_system',
    packages=find_packages(exclude=('tests', 'docs'))
)