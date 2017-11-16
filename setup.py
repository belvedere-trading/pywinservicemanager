from setuptools import setup, find_packages
import subprocess
import platform
import sys
import re

tag_regex = re.compile(r'^v\d+\.\d+\.\d+$')
def get_version():
    version = ''
    with open('version.txt') as file:
        version = file.read()
    version = version.strip()
    if not re.match(tag_regex, version):
        print 'Found invalid tag: {}'.format(version)
        sys.exit(-1)
    return version

if __name__ == '__main__':
    is_windows = any(platform.win32_ver())
    required_packages = []
    if is_windows:
        required_packages = open('required_packages.req').read().splitlines()
    testPackages = open('test_required_packages.req').read().splitlines()


setup(name='pywinservicemanager',
      version=get_version(),
      author='Team Belvedere, LLC',
      author_email='opensource@belvederetrading.com',
      url='https://github.com/belvedere-trading/pywinservicemanager',
      license=open('LICENSE.txt').read(),
      description='Windows Service Manager Module that wraps for the win32service api',
      packages=find_packages(),
      long_description=open('README.rst').read(),
      install_requires=required_packages,
      tests_require=testPackages)
