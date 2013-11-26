set -e

export DEBIAN_FRONTEND=noninteractive

apt-get update -yq
apt-get install -y curl

curl get.docker.io | sh

curl -L -o /usr/bin/loggly-pipe \
    https://raw.github.com/modcloth-labs/loggly-pipe/master/loggly_pipe.py
chmod +x /usr/bin/loggly-pipe

cp -v /vagrant/example-app.conf /etc/init/example-app.conf

cd /vagrant
./build-container

start example-app
