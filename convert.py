import requests
import time
import os
import logging
import sys
import raven
import calendar
from datetime import datetime

# 生成 logger 对象
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 集成 raven
client = None
raven_sdn = os.getenv('RAVEN_SDN', None)
if raven_sdn:
    client = raven.Client(
        dsn=raven_sdn
    )


def querify(params, prefix=','):
    """
    把 {a:1,b:2} 转换成 ,a=1,b=1 的格式
    :param params: dict
    :return: str
    """
    items = params.items()
    if len(items) == 0:
        return ''
    tags = [str(k) + '=' + str(v) for (k, v) in items]
    return prefix + ','.join(sorted(tags))


def line(obj):
    """
    把 dict 转成 string， 参考 http://opentsdb.net/docs/build/html/api_http/stats/index.html
    :param obj: dict
    :return: str
    """
    return '{metric}{tags} value={value} {timestamp}000000000'.format(
        metric=obj['metric'],
        timestamp=obj['timestamp'],
        value=obj['value'],
        tags=querify(obj['tags'])
    )


def now():
    now = datetime.utcnow()
    timestamp = int(calendar.timegm(now.timetuple()) * 1000 + now.microsecond / 1000)
    return timestamp


def line_region_client(obj):
    values = {}
    tags = {}

    for (k, v) in obj.items():
        if isinstance(v, str):
            tags[k] = v
        elif isinstance(v, bool):
            pass
        elif isinstance(v, int):
            values[k] = v

    return 'regionClient{tags} {value} {timestamp}000000'.format(
        timestamp=now(),
        value=querify(values, ''),
        tags=querify(tags)
    )


def convert_stats(obj):
    """
    :param obj:
    :return:
    """
    return '\n'.join([line(item) for item in obj])


def convert_region_clients(obj):
    return '\n'.join([line_region_client(item) for item in obj])


def pipe(opentsdb_url, influxdb_url, timeout):
    """
    请求 Opentsdb => 转换格式 => 发送到 Influxdb
    :return:
    """

    def write_data(data):
        d = requests.post(influxdb_url, proxies={
            "http": None
        }, data=data)
        status_code = d.status_code

        # http://opentsdb.net/docs/build/html/api_http/index.html#response-codes
        if status_code in [200, 204]:
            logger.info('[%d] pipe success' % d.status_code)
        else:
            logger.error('[%d] pipe error:\n%s' % (d.status_code, d.text))

    res = requests.get(opentsdb_url + 'api/stats', timeout=timeout)
    write_data(convert_stats(res.json()))

    rcs = requests.get(opentsdb_url + 'api/stats/region_clients', timeout=timeout)
    write_data(convert_region_clients(rcs.json()))


if __name__ == '__main__':
    # 从环境变量中读取配置

    interval = int(os.getenv('INTERVAL', '10'))
    opentsdb_url = os.getenv('OPENTSDB_URL', None)
    influxdb_url = os.getenv('INFLUXDB_URL', None)

    logger.info('interval=%d' % interval)
    logger.info('opentsdb_url=%s' % opentsdb_url)
    logger.info('influxdb_url=%s' % influxdb_url)

    if not opentsdb_url or not influxdb_url:
        sys.exit()

    while True:
        try:
            pipe(
                opentsdb_url=opentsdb_url,
                influxdb_url=influxdb_url,
                timeout=interval / 2
            )
        except BaseException as e:
            logger.error(e)
            if client:
                client.captureException()
        finally:
            time.sleep(interval)
