import os
import sys
import warnings

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

install_requires = []
install_requires = [
    'pandas==0.20.0rc1',
    'requests>=2.13.0',
    'uuid>=1.30',
    'unittest2>=1.1.0',
    'simplejson>=3.10.0',
]

if sys.version_info < (2, 7):
    warnings.warn(
        'Python 2.7 is no longer officially supported by RedTen. '
        'If you have any questions, please file an issue on Github or '
        'contact us at https://github.com/jay-johnson/redten-python',
        DeprecationWarning)

import unittest
def redten_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

# Don't import redten module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'redten'))

setup(
    name='redten',
    cmdclass={'build_py': build_py},
    version='1.0.1',
    description='Red10 distributed machine learning python client',
    long_description='Red10 distributed machine learning python client',
    author='Red10',
    author_email='jay.p.h.johnson@gmail.com',
    url='https://github.com/jay-johnson/redten-python',
    packages=['redten'],
    package_data={},
    install_requires=install_requires,
    test_suite='setup.redten_test_suite',
    tests_require=['unittest2', 'mock'],
    use_2to3=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])
