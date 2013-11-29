# vim:fileencoding=utf-8
"""
Packaging bits!
"""
from __future__ import print_function

import ast
import sys
from subprocess import check_output

from setuptools import setup

PY3 = sys.version >= '3'


def get_version():
    """
    Get the version from the source, but without importing.
    """
    with open('loggly_pipe.py') as source:
        for node in ast.walk(ast.parse(source.read(), 'loggly_pipe.py')):
            if node.__class__.__name__ == 'Assign' and \
               '__version__' in ast.dump(node.targets[0]):
                return node.value.s


def get_long_description():
    """
    Use the ``README.rst`` as the long description.
    """
    with open('README.rst') as readme:
        return readme.read().strip()


setup(
    name='loggly_pipe',
    author='Dan Buch',
    author_email='d.buch@modcloth.com',
    license='MIT',
    keywords='loggly logging http logs',
    url='https://github.com/modcloth-labs/loggly-pipe',
    description='Pipe stuff to Loggly.',
    long_description=get_long_description(),
    version=get_version(),
    py_modules=['loggly_pipe'],
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: SunOS/Solaris',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: System :: Logging',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'loggly-pipe = loggly_pipe:main'
        ]
    }
)
