import requests
import time
import os
import logging
import sys


def querify(params):
    if len(params) == 0:
        return ''
    tags = [k + '=' + v for (k, v) in params.items()]

    return ',' + ','.join(tags)


def convert(obj):
    return '{metric}{tags} value={value} {timestamp}000000000'.format(
        metric=obj['metric'],
        timestamp=obj['timestamp'],
        value=obj['value'],
        tags=querify(obj['tags'])
    )


def main():
    opentsdb_url = os.getenv('OPENTSDB_URL', None)
    influxdb_url = os.getenv('INFLUXDB_URL', None)

    if not opentsdb_url or not influxdb_url:
        sys.exit()

    res = requests.get(opentsdb_url, timeout=1)

    payload_lines = [convert(item) for item in res.json()]
    d = requests.post(influxdb_url, proxies={
        "http": None
    }, data='\n'.join(payload_lines))

    logging.info('[%d] write %d records' % (d.status_code, len(payload_lines)))


if __name__ == '__main__':
    while True:
        try:
            main()
        except BaseException as e:
            logging.error(e)
        finally:
            time.sleep(20)
