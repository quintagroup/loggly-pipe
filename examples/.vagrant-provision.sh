#!/bin/bash
set -e

export DEBIAN_FRONTEND=noninteractive

apt-get update -yq
apt-get install -y curl python2.7

if ! which docker >/dev/null ; then
  curl https://get.docker.io | sh
fi

curl -L -o /usr/bin/loggly-pipe \
    https://raw.github.com/modcloth-labs/loggly-pipe/master/loggly_pipe.py
chmod +x /usr/bin/loggly-pipe

cp -v /vagrant/example-app.conf /etc/init/example-app.conf
cp -v /vagrant/fake-loggly.conf /etc/init/fake-loggly.conf

cd /vagrant
./build-container

stop fake-loggly || true
start fake-loggly
while ! curl -s localhost:9090 >/dev/null ; do
  sleep 0.1
done

stop example-app || true
start example-app
