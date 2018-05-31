#! /bin/sh
docker run -it -p 8888:8888 -p 6006:6006 -v /vagrant/tensorflow:/notebooks my-tensorflow $1
