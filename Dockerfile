FROM python:3.6
ADD . .
ENV OPENTSDB_URL http://opentsdb:4246
ENV INFLUXDB_URL http://influxdb:8086
ENV INTERVAL 10
ENV SENTRY_RELEASE v0.5.0
RUN pip install -v -r requirements.txt
CMD ["python","./convert.py"]