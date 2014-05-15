from setuptools import setup, find_packages
from glob import glob
import re

package_name = 'srw'
version_str = re.search(r'^__version__\s+=\s+[\'"]([\d.]+)[\'"]',
        open('%s/version.py' % (package_name, )).read(),
        re.M).group(1)

setup(name=package_name,
        version=version_str,
        description='Utility python code',
        author='Simon Walker',
        author_email='s.r.walker101@googlemail.com',
        url='http://github.com/mindriot101/srwmodule',
        packages=find_packages(),
        long_description=open('README.md').read(),
        install_requires=[],
        )
