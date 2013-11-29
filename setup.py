# vim:fileencoding=utf-8

import sys
from subprocess import check_output

from setuptools import setup

PY3 = sys.version >= '3'


def get_version():
    raw_version = check_output(
        ['git', 'describe', '--always', '--tags']
    ).strip()
    if PY3:
        raw_version = raw_version.decode('UTF-8')
    return raw_version.replace('v', '')


setup(
    name='loggly_pipe',
    author='Dan Buch',
    author_email='d.buch@modcloth.com',
    license='MIT',
    keywords='loggly logging http logs',
    url='https://github.com/modcloth-labs/loggly-pipe',
    description='Pipe stuff to Loggly.',
    version=get_version(),
    py_modules=['loggly_pipe'],
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
