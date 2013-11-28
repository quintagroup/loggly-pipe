#!/usr/bin/env python
# vim:fileencoding=utf-8
"""
It's ``loggly-pipe``, nerds!
"""
from __future__ import print_function, unicode_literals

import json
import os
import sys
import time
import threading

try:
    from queue import Queue # pylint: disable=F0401
except ImportError:
    from Queue import Queue # pylint: disable=F0401


def main():
    """
    Read configuration from ``os.environ``, then eat and poop JSON forevar.
    """
    cfg = _get_config(os.environ)
    if cfg['debug']:
        json.dump({'_config': cfg}, sys.stderr)
        print('', file=sys.stderr)

    line_queue = Queue()
    flusher = threading.Thread(
        name='flusher',
        target=_flush_tick,
        args=(line_queue, cfg['flush_interval'])
    )
    shipper = threading.Thread(
        name='shipper',
        target=_shipper_loop,
        args=(line_queue, cfg['batch_size'], cfg['log_url'])
    )
    flusher.daemon = True
    flusher.start()
    shipper.start()

    def cleanup():
        """
        Closes down the queue and shipper the nice way.
        """
        line_queue.put('___FLUSH___')
        line_queue.put('___EXIT___')
        shipper.join()

    i = 1
    try:
        for line in _input_lines(cfg['sleep_interval']):
            print(line, file=sys.stdout, end='')
            line_queue.put(line.strip())
            i += 1
            if i > cfg['max_lines']:
                cleanup()
                return 0
        return 0
    except (KeyboardInterrupt, IOError):
        cleanup()
        return 0


def _flush_tick(line_queue, interval):
    """
    Sends periodic flushes to the line queue.
    """
    while True:
        time.sleep(interval)
        line_queue.put('___FLUSH___')


def _shipper_loop(line_queue, batch_size, log_url):
    """
    Accumulates and ships batches of lines to ``log_url``.
    """
    try:
        while True:
            buf = []

            for _ in range(batch_size):
                line = line_queue.get()
                if line == '___EXIT___':
                    _ship_batch(buf, log_url)
                    return True

                elif line == '___FLUSH___':
                    _ship_batch(buf, log_url)
                    buf = []
                else:
                    buf.append(('PLAINTEXT', line))

            _ship_batch(buf, log_url)

    except (OSError, IOError) as err:
        json.dump({'error': str(err)}, sys.stderr)
        print('', file=sys.stderr)
        return False


def _ship_batch(buf, log_url):
    """
    Performs the URL encoding and HTTP fun.
    """
    if not buf:
        return

    try:
        from urllib.request import urlopen # pylint: disable=E0611,F0401
        from urllib.parse import urlencode # pylint: disable=E0611,F0401
    except ImportError:
        from urllib import urlopen, urlencode # pylint: disable=E0611

    from datetime import datetime

    response = urlopen(log_url, urlencode(buf).encode('UTF-8')).read().strip()
    json.dump({
        '_mark': datetime.utcnow().isoformat(),
        'result': response.decode('UTF-8')
    }, sys.stderr)
    print('', file=sys.stderr)


def _get_config(env):
    """
    Reads configuration from dict-like env, coercing and defaulting as needed.
    """
    token = env['LOGGLY_TOKEN']

    tags = env.get('LOGGLY_TAGS', 'python')
    loggly_server = env.get('LOGGLY_SERVER', 'https://logs-01.loggly.com')

    batch_size = int(env.get('LOGGLY_BATCH_SIZE', '100'))
    max_lines = int(env.get('LOGGLY_MAX_LINES', '10000'))
    debug = env.get('DEBUG') is not None
    sleep_interval = float(env.get('LOGGLY_STDIN_SLEEP_INTERVAL', '0.1'))
    flush_interval = float(env.get('LOGGLY_FLUSH_INTERVAL', '10.0'))

    log_url = '{}/inputs/{}/tag/{}/'.format(loggly_server, token, tags)

    return {
        'batch_size': batch_size,
        'max_lines': max_lines,
        'debug': debug,
        'sleep_interval': sleep_interval,
        'flush_interval': flush_interval,
        'log_url': log_url
    }


def _input_lines(sleep_interval=0.1):
    """
    Reads lines from stdin, dangit.
    """
    while True:
        if sys.stdin.closed:
            raise StopIteration

        line = sys.stdin.readline().decode('UTF-8')
        stripped = line.strip()
        if not stripped:
            time.sleep(sleep_interval)
            continue

        yield line


if __name__ == '__main__':
    sys.exit(main())
