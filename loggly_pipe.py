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
    _debug = _debug_func(cfg['debug'])
    _debug({'msg': 'dumping config', 'config': cfg})

    line_queue = Queue()
    exc_queue = Queue()
    flusher = threading.Thread(
        name='flusher',
        target=_flush_tick,
        args=(line_queue, cfg['flush_interval'])
    )

    shippers = []
    for i in range(cfg['n_shippers']):
        shipper = threading.Thread(
            name='shipper-{}'.format(i),
            target=_shipper_loop,
            args=(
                line_queue,
                exc_queue,
                cfg['batch_size'],
                cfg['log_url'],
                cfg['n_attempts']
            )
        )
        _debug({'msg': 'adding shipper', 'shipper': shipper.name})
        shippers.append(shipper)

    flusher.daemon = True
    flusher.start()

    for shipper in shippers:
        shipper.daemon = True
        _debug({'msg': 'starting shipper', 'shipper': shipper.name})
        shipper.start()

    def cleanup():
        """
        Closes down the queue and shipper the nice way.
        """
        _debug({'msg': 'cleaning up threads'})
        for shipper in shippers:
            line_queue.put('___FLUSH___')
            line_queue.put('___EXIT___')
            _debug({'msg': 'joining shipper', 'shipper': shipper.name})
            shipper.join(0.1)

    i = 1
    try:
        for line in _input_lines(cfg['sleep_interval']):
            print(line, file=sys.stdout, end='')
            _debug({'msg': 'queuing line'})
            line_queue.put(line.strip())

            if not exc_queue.empty():
                exc = exc_queue.get()
                exc_queue.task_done()
                _debug({'msg': 'received on error queue', 'exc': str(exc)})
                if exc != None and cfg['exc_behavior'] == 'raise':
                    _debug({'msg': 'raising error', 'exc': str(exc)})
                    raise RuntimeError(exc)

            i += 1
            if cfg['max_lines'] != 0 and i > cfg['max_lines']:
                _debug({'msg': 'hit max_lines'})
                cleanup()
                return 0

        return 0
    except (KeyboardInterrupt, OSError, IOError) as exc:
        _debug({'msg': 'caught exception', 'exc': str(exc)})
        cleanup()
        return 0


def _debug_func(is_debug):
    """
    Generate a debugging function that's only fired if ``is_debug`` is truthy
    """
    def _debug(msg, **kwargs):
        """
        Conditionally ``json.dumps(msg)`` to stderr
        """
        if not is_debug:
            return
        if not 'file' in kwargs:
            kwargs['file'] = sys.stderr
        msg['_debug'] = 1
        print(json.dumps(msg), **kwargs)
    return _debug


def _flush_tick(line_queue, interval):
    """
    Sends periodic flushes to the line queue.
    """
    while True:
        time.sleep(interval)
        line_queue.put('___FLUSH___')


def _shipper_loop(line_queue, exc_queue, batch_size, log_url, attempts):
    """
    Accumulates and ships batches of lines to ``log_url``.
    """
    try:
        while True:
            buf = []

            for _ in range(batch_size):
                line = line_queue.get()
                if line == '___EXIT___':
                    _ship_batch(buf, log_url, attempts)
                    line_queue.task_done()
                    return True

                elif line == '___FLUSH___':
                    _ship_batch(buf, log_url, attempts)
                    line_queue.task_done()
                    buf = []
                else:
                    buf.append(('PLAINTEXT', line))

            _ship_batch(buf, log_url, attempts)
            line_queue.task_done()

    except (OSError, IOError) as exc:
        json.dump({'error': str(exc)}, sys.stderr)
        print('', file=sys.stderr)
        exc_queue.put(exc)


def _ship_batch(buf, log_url, attempts=1):
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

    body = urlencode(buf).encode('UTF-8')
    n_attempt = 0
    while True:
        try:
            response = urlopen(log_url, body).read().strip()
            json.dump({
                '_mark': datetime.utcnow().isoformat(),
                'result': response.decode('UTF-8')
                }, sys.stderr)
            print('', file=sys.stderr)
            return
        except (IOError, OSError):
            n_attempt += 1
            if n_attempt == attempts:
                raise


def _get_config(env):
    """
    Reads configuration from dict-like env, coercing and defaulting as needed.
    """
    token = env['LOGGLY_TOKEN']

    tags = env.get('LOGGLY_TAGS', 'python')
    loggly_server = env.get('LOGGLY_SERVER', 'https://logs-01.loggly.com')

    batch_size = int(env.get('LOGGLY_BATCH_SIZE', '100'))
    max_lines = int(env.get('LOGGLY_MAX_LINES', '0'))
    n_attempts = int(env.get('LOGGLY_SHIP_ATTEMPTS', '1'))

    n_shippers = int(env.get('LOGGLY_SHIPPER_COUNT', '1'))

    is_debug = env.get('LOGGLY_DEBUG') is not None
    sleep_interval = float(env.get('LOGGLY_STDIN_SLEEP_INTERVAL', '0.1'))
    flush_interval = float(env.get('LOGGLY_FLUSH_INTERVAL', '10.0'))
    exc_behavior = env.get('LOGGLY_ON_ERROR', 'raise')

    log_url = '{}/inputs/{}/tag/{}/'.format(loggly_server, token, tags)

    return {
        'batch_size': batch_size,
        'max_lines': max_lines,
        'n_attempts': n_attempts,
        'debug': is_debug,
        'n_shippers': n_shippers,
        'sleep_interval': sleep_interval,
        'flush_interval': flush_interval,
        'exc_behavior': exc_behavior,
        'log_url': log_url
    }


def _input_lines(sleep_interval=0.1):
    """
    Reads lines from stdin, dangit.
    """
    while True:
        if sys.stdin.closed:
            raise StopIteration

        line = sys.stdin.readline()
        if hasattr(line, 'decode'):
            line = line.decode('UTF-8')

        stripped = line.strip()
        if not stripped:
            time.sleep(sleep_interval)
            continue

        yield line


if __name__ == '__main__':
    sys.exit(main())
