#!/usr/bin/env python
# vim:fileencoding=utf-8
"""
Pretends to be Loggly, or really just a black hole.
"""
from __future__ import print_function, unicode_literals

import sys
try:
    from urllib.parse import parse_qsl # pylint: disable=F0401,E0611
except ImportError:
    from urlparse import parse_qsl # pylint: disable=F0401

if sys.version < '3':
    OK = b'200 OK'
    METHOD_NOT_ALLOWED = b'405 Method Not Allowed'
    CTYPE_JSON = (b'content-type', b'application/json')
else:
    OK = '200 OK'
    METHOD_NOT_ALLOWED = '405 Method Not Allowed'
    CTYPE_JSON = ('content-type', 'application/json')


def main():
    """
    Fire up a li'l WSGI app, people.
    """
    import os
    from wsgiref.simple_server import make_server

    host, port = '127.0.0.1', int(os.environ.get('PORT', '9090'))
    server = make_server(host, port, fake_loggly_server)

    print('Serving on {}:{}'.format(host, port), file=sys.stderr)
    server.serve_forever()


def fake_loggly_server(environ, start_response):
    """
    GETs and POSTs are 200, mkay!
    """
    if environ['REQUEST_METHOD'] == 'GET':
        start_response(OK, [CTYPE_JSON])
        return [b'{"result":"meh"}\n']
    elif environ['REQUEST_METHOD'] == 'POST':
        start_response(OK, [CTYPE_JSON])
        if environ['CONTENT_LENGTH']:
            body = environ['wsgi.input'].read(
                int(environ['CONTENT_LENGTH'])
            )
            sys.stdout.flush()
            for _, value in parse_qsl(body):
                print('===> {!r}'.format(value))
                sys.stdout.flush()

        return [b'{"result":"ok"}\n']
    else:
        start_response(METHOD_NOT_ALLOWED, [CTYPE_JSON])
        return [b'{"result":"hosed"}\n']


if __name__ == '__main__':
    sys.exit(main())
