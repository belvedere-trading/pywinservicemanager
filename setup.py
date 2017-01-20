from setuptools import setup, find_packages
import sys


setup(name='pywinservicemanager',
      version='1.0.2',
      author='Team Belvedere, LLC',
      author_email='opensource@belvederetrading.com',
      url='https://github.com/belvedere-trading/pywinservicemanager',
      license=open('LICENSE.txt').read(),
      description='Windows Service Manager Module that wraps for the win32service api',
      packages=find_packages(),
      long_description=open('README.rst').read(),
      install_requires=['pypiwin32>=219'],
      tests_require=['mock', 'nose'])
