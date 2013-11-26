#!/usr/bin/env python
# vim:fileencoding=utf-8
"""
It's ``loggly-pipe``, nerds!
"""
from __future__ import print_function

import json
import os
import urllib
import sys

from datetime import datetime


def main():
    """
    Read configuration from ``os.environ``, then eat and poop JSON forevar.
    """
    cfg = _get_config(os.environ)
    i = 1

    if cfg['debug']:
        json.dump({'_config': cfg}, sys.stderr)
        print('', file=sys.stderr)

    try:
        while True:
            if i > cfg['max_loops']:
                return 0

            for record in _ship_a_batch(cfg['batch_size'], cfg['log_url']):
                if record['type'] == 'line':
                    sys.stdout.write(record['line'])
                    sys.stdout.flush()

                elif record['type'] == 'mark':
                    json.dump({
                        '_mark': record['timestamp'].isoformat(),
                        'result': record['result']
                    }, sys.stderr)
                    print('', file=sys.stderr)

            i += 1

    except (KeyboardInterrupt, IOError):
        return 0


def _get_config(env):
    """
    Reads configuration from dict-like env, coercing and defaulting as needed.
    """
    token = env['LOGGLY_TOKEN']

    tag = env.get('LOGGLY_TAG', 'python')
    loggly_server = env.get('LOGGLY_SERVER', 'https://logs-01.loggly.com')

    batch_size = int(env.get('LOGGLY_BATCH_SIZE', '100'))
    max_loops = int(env.get('LOGGLY_MAX_LOOPS', '10000'))
    debug = env.get('DEBUG') is not None

    log_url = '{}/inputs/{}/tag/{}/'.format(loggly_server, token, tag)

    return {
        'batch_size': batch_size,
        'max_loops': max_loops,
        'debug': debug,
        'log_url': log_url
    }


def _ship_a_batch(batch_size, log_url):
    """
    Buffers up a list of lines, then URL-encodes and POSTs to Loggly.
    """
    buf = []

    for _ in range(batch_size):
        line = sys.stdin.readline()
        stripped = line.strip()
        if not stripped:
            continue

        buf.append(('PLAINTEXT', stripped))
        yield {
            'type': 'line',
            'line': line
        }

    if buf:
        yield {
            'type': 'mark',
            'timestamp': datetime.utcnow(),
            'result': urllib.urlopen(log_url, urllib.urlencode(buf)).read()
        }


if __name__ == '__main__':
    sys.exit(main())
