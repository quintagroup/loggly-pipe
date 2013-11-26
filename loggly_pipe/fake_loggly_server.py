#!/usr/bin/env python
# vim:fileencoding=utf-8
import sys


def fake_loggly_server(environ, start_response):
    start_response('200 OK', [
        ('content-type', 'application/json'),
    ])
    return ['{"result":"ok"}\n']


def main():
    import os
    from wsgiref.simple_server import make_server

    host, port = '127.0.0.1', int(os.environ.get('PORT', '9090'))
    server = make_server(host, port, fake_loggly_server)

    print 'Serving on {}:{}'.format(host, port)
    server.serve_forever()


if __name__ == '__main__':
    sys.exit(main())
