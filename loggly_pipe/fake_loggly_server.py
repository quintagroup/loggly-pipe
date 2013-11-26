#!/usr/bin/env python
# vim:fileencoding=utf-8
"""
Pretends to be Loggly, or really just a black hole.
"""
from __future__ import print_function

import sys


def main():
    """
    Fire up a li'l WSGI app, people.
    """
    import os
    from wsgiref.simple_server import make_server

    host, port = '127.0.0.1', int(os.environ.get('PORT', '9090'))
    server = make_server(host, port, fake_loggly_server)

    print('Serving on {}:{}'.format(host, port))
    server.serve_forever()


def fake_loggly_server(environ, start_response):
    """
    GETs and POSTs are 200, mkay!
    """
    if environ['REQUEST_METHOD'] in ('GET', 'POST'):
        start_response('200 OK', [
            ('content-type', 'application/json'),
        ])
        return ['{"result":"ok"}\n']
    else:
        start_response('405 Method Not Allowed', [
            ('content-type', 'application/json'),
        ])
        return ['{"result":"hosed"}\n']


if __name__ == '__main__':
    sys.exit(main())
