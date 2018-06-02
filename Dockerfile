#FROM gcr.io/tensorflow/tensorflow
FROM gcr.io/tensorflow/tensorflow:latest-py3

RUN set -x && \
    apt-get update && \
    apt-get install -y vim && \
    pip3 install -U pip && \
    pip3 install kaggle && \
    pip3 install requests && \
    pip3 install keras

RUN set -x && \
    pip3 install seaborn && \
    apt-get install -y python3-tk

ADD kaggle.json /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json

ADD keras.json /root/.keras/keras.json

EXPOSE 9987
EXPOSE 6006

CMD ["/run_jupyter.sh", "--allow-root", "--port=9987"]
