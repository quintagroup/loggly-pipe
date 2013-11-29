``loggly-pipe``
===============

.. image:: https://travis-ci.org/modcloth-labs/loggly-pipe.png?branch=master
   :target: https://travis-ci.org/modcloth-labs/loggly-pipe

* Eats JSON from stdin.
* Sends batches to Loggly (or compatible).
* Poops unaltered JSON to stdout.
* Poops ``mark`` JSON to stdout.

Installation
------------

``loggly-pipe`` is built to be executed as a standalone file, so installing
directly from the raw github URL works great:

.. code-block:: bash

    curl -L -o loggly-pipe https://raw.github.com/modcloth-labs/loggly-pipe/master/loggly_pipe.py
    chmod +x loggly-pipe

Configuration
-------------

All configuration is env-based:

* ``LOGGLY_TOKEN`` **REQUIRED** one of the tokens from your Loggly account
* ``LOGGLY_SERVER`` the base server URI (default
  ``https://logs-01.loggly.com``)
* ``LOGGLY_SHIPPER_COUNT`` number of shipper threads (default ``1``)
* ``LOGGLY_TAGS`` comma-delimited tags to apply to the shipped records.
  This is passed directly as the last member of ``PATH_INFO``, so it
  should be URL-encoded if necessary.  (default ``python``)
* ``LOGGLY_BATCH_SIZE`` number of records to accumulate before shipping
  over HTTP (default ``100``)
* ``LOGGLY_MAX_LINES`` exit after consuming this many lines (default ``0``,
  which disables)
* ``LOGGLY_STDIN_SLEEP_INTERVAL`` interval in seconds to sleep when line
  read from stdin is empty (default ``0.1``)
* ``LOGGLY_FLUSH_INTERVAL`` interval in seconds at which to flush the line
  buffer so that low activity doesn't cause records to back up (default
  ``10.0``)
* ``LOGGLY_SHIP_ATTEMPTS`` number of times to retry each batch over HTTP
  (default ``1``)
* ``LOGGLY_ON_ERROR`` behavior when exceptions are caught, which is
  usually around shipping over HTTP, and will only take effect once
  ``LOGGLY_SHIP_ATTEMPTS`` has been reached (choices are ``raise``, ``ignore``;
  default ``raise``)
* ``LOGGLY_DEBUG`` print some debuggy stuff if non-empty

Usage
-----

Given a stdin stream made of line-based JSON records, ``loggly-pipe`` will
emit each record unaltered as well as a record with a single ``_mark`` key
for each batch.

Here's an example of a node app that uses bunyan for logging as well as
the ``bunyan`` command line tool for human readability:

.. code-block:: bash

    node server.js | loggly-pipe | bunyan

A trivial example that's used in the black-box test of ``loggly-pipe``
itself can be found in the `examples dir <./examples>`_.
