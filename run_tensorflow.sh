#! /bin/sh
export PROJECT_ROOT=$(dirname "$0")
cd ${PROJECT_ROOT}

docker build -t kapa ./

docker run -it -p 8888:8888 -p 6006:6006 -v ${PWD}:/notebooks kapa $1
