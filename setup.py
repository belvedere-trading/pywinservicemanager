from setuptools import setup, find_packages
import sys

if __name__ == '__main__':
    if not sys.platform.startswith('win'):
        raise OSError('This module is only supported on Windows systems')

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(name='pywinservicemanager',
      version='1.0.0',
      author='Team Belvedere, LLC',
      author_email=''
      license=open('LICENSE.txt').read(),
      description='Windows Service Manager Module that wraps for the win32service api',
      packages=find_packages(),
      long_description=long_description,
      install_requires=['pywin32>=214'],
      tests_require=['mock', 'nose'])
