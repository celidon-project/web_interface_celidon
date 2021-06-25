FROM python:3.7

RUN pip install --no-cache-dir paho-mqtt==1.5.0 \
                               websockets==8.1

COPY position_server.py /position_server.py

ENTRYPOINT [ "python3", "position_server.py" ]
