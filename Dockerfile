FROM python:3.6
ADD . .
ENV OPENTSDB_URL http://tunnel:4246
ENV INFLUXDB_URL http://influxdb:8086
RUN pip install -v -r requirements.txt
CMD ["python","./convert.py"]