`loggly-pipe`
=============

[![Build Status](https://travis-ci.org/modcloth-labs/loggly-pipe.png)](https://travis-ci.org/modcloth-labs/loggly-pipe)

- Eats JSON from stdin.
- Sends batches to Loggly (or compatible).
- Poops unaltered JSON to stdout.
- Poops `mark` JSON to stdout.

## Installation

`loggly-pipe` is built to be executed as a standalone file, so
installing directly from the raw github URL works great:

``` bash
curl -L -o loggly-pipe https://raw.github.com/modcloth-labs/loggly-pipe/master/loggly_pipe.py
chmod +x loggly-pipe
```

## Configuration

All configuration is env-based:

- `LOGGLY_TOKEN` **REQUIRED** one of the tokens from your Loggly account
- `LOGGLY_SERVER` the base server URI (default
  `https://logs-01.loggly.com`)
- `LOGGLY_TAG` tag to apply to the shipped records (default `python`)
- `LOGGLY_BATCH_SIZE` number of records to accumulate before shipping
  over HTTP (default `100`)

## Usage

Given a stdin stream made of line-based JSON records, `loggly-pipe` will
emit each record unaltered as well as a record with a single `_mark` key
for each batch.

Here's an example of a node app that uses bunyan for logging as well as
the `bunyan` command line tool for human readability:

``` bash
node server.js | loggly-pipe | bunyan
```

A trivial example that's used in the black-box test of `loggly-pipe`
itself can be found in the [examples dir](./examples).
