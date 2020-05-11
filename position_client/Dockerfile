FROM python:3.7

RUN pip install --no-cache-dir paho-mqtt==1.5.0

COPY . /

ENTRYPOINT [ "python3", "./position_client.py" ]
