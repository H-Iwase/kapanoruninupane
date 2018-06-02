#! /bin/sh
export PROJECT_ROOT="$(dirname \"$0\")"
cd ${PROJECT_ROOT}

set -e

docker build -t kapa ./

docker run -it -p 9987:9987 -p 6006:6006 -v ${PWD}:/notebooks kapa $1
