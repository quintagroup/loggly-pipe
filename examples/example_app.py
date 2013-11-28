#!/usr/bin/env python
# vim:fileencoding=utf-8
"""
A little example JSON-making thing.
"""

import sys
import os
import json
from random import randint


def main():
    """
    Dump random JSON records to stdout ``os.environ['LOOPS']`` times.
    """
    for i in range(int(os.environ.get('LOOPS', '100'))):
        json.dump({
            'foo': randint(0, 1000),
            'i': i
        }, sys.stdout)
        print('')
    return 0


if __name__ == '__main__':
    sys.exit(main())
