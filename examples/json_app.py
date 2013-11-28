#!/usr/bin/env python
# vim:fileencoding=utf-8
"""
A little example JSON-making thing.
"""

import sys
import os
import json
from random import randint
from datetime import datetime


def main():
    """
    Dump random JSON records to stdout ``os.environ['LOOPS']`` times.
    """
    max_loops = int(os.environ.get('LOOPS', '0'))
    n_loop = 0

    while max_loops == 0 or n_loop < max_loops:
        json.dump({
            'wat': randint(0, 1000),
            'timestamp': datetime.utcnow().isoformat()
        }, sys.stdout)
        print('')
        n_loop += 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
