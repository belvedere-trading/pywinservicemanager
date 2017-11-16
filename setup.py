from setuptools import setup, find_packages
import subprocess
import platform
import sys
import re

tag_regex = re.compile(r'v\d\.\d\.\d')
def get_tagged_version():
    process = subprocess.Popen(['git', 'describe', '--abbrev=0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode:
        print 'Failed to get tagged version: {}'.format(err)
        sys.exit(process.returncode)
    out = out.strip()
    if not re.match(tag_regex, out):
        print 'Found invalid tag: {}'.format(out)
        sys.exit(-1)
    return out[1:]

if __name__ == '__main__':
    is_windows = any(platform.win32_ver())
    required_packages = []
    if is_windows:
        required_packages = open('required_packages.req').read().splitlines()
    testPackages = open('test_required_packages.req').read().splitlines()


setup(name='pywinservicemanager',
      version=get_tagged_version(),
      author='Team Belvedere, LLC',
      author_email='opensource@belvederetrading.com',
      url='https://github.com/belvedere-trading/pywinservicemanager',
      license=open('LICENSE.txt').read(),
      description='Windows Service Manager Module that wraps for the win32service api',
      packages=find_packages(),
      long_description=open('README.rst').read(),
      install_requires=required_packages,
      tests_require=testPackages)
