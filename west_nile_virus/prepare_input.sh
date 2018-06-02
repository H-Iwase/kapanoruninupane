#!/bin/sh

set -e

INPUT_DIR="./input"

kaggle competitions download -c predict-west-nile-virus -p ${INPUT_DIR}
cd ${INPUT_DIR}
unzip \*.zip
rm *.zip