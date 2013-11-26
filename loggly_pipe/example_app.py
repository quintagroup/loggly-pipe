#!/usr/bin/env python
# vim:fileencoding=utf-8

import sys
import os
import json
from random import randint


def main():
    for i in range(int(os.environ['LOOPS'])):
        json.dump({'foo': randint(0, 1000)}, sys.stdout)
        print('')
    return 0


if __name__ == '__main__':
    sys.exit(main())
