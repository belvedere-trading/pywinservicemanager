from setuptools import setup, find_packages
import platform

is_windows = any(platform.win32_ver())
required_packages = []
if is_windows:
      required_packages = ['pypiwin32>=219']

setup(name='pywinservicemanager',
      version='1.0.3',
      author='Team Belvedere, LLC',
      author_email='opensource@belvederetrading.com',
      url='https://github.com/belvedere-trading/pywinservicemanager',
      license=open('LICENSE.txt').read(),
      description='Windows Service Manager Module that wraps for the win32service api',
      packages=find_packages(),
      long_description=open('README.rst').read(),
      install_requires=required_packages,
      tests_require=['mock', 'nose'])
