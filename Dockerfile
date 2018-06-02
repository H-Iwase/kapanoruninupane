#FROM gcr.io/tensorflow/tensorflow
FROM gcr.io/tensorflow/tensorflow:latest-py3

RUN set -x && \
    apt-get update && \
    apt-get install -y vim && \
    apt-get install -y python3-tk

RUN set -x && \
    pip3 install --upgrade pip && \
    pip3 install seaborn && \
    pip3 install geopy && \
    pip3 install requests && \
    pip3 install keras && \
    pip3 install lightgbm


ADD keras.json /root/.keras/keras.json

EXPOSE 8888
EXPOSE 6006
