#FROM gcr.io/tensorflow/tensorflow
FROM gcr.io/tensorflow/tensorflow:latest-py3

RUN set -x && \
    apt-get update && \
    apt-get install -y vim && \
    pip3 install requests && \
    pip3 install keras

RUN set -x && \
    pip3 install seaborn && \
    apt-get install -y python3-tk

ADD keras.json /root/.keras/keras.json

EXPOSE 8888
EXPOSE 6006
