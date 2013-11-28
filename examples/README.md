`loggly-pipe` example apps
==========================

This directory contains two different applications, one which emits JSON log
records and the other that produces more traditional line-based log records.
There is also a smallish HTTP application that pretends to be Loggly.  To get
started do the vagrant dance:

``` bash
vagrant up
```

During vagrant provisioning, docker will be installed and a little container
will be built containing the contents of this directory.  Additionally, an
upstart configuration will be written for each example app and the fake Loggly
HTTP application.

The fake Loggly application will be started during provision as well, but the
example `json-app` and `line-app` jobs *will not* be started, mostly because
they loop forever by default and typically end up pegging the CPU.  To start
them by hand, do something like so:

``` bash
vagrant ssh
sudo start json-app
sudo start line-app
```
