import requests
import time


def convert(input_str):
    splited = input_str.split()
    if len(splited) < 4:
        return None

    (metricName, time, value, *tags) = splited

    return metricName + ',' + ','.join(tags) + ' value=' + value + ' ' + time + '000000000'


def main():
    res = requests.get("http://tunnel:4246/stats", timeout=5)
    converted = filter(lambda s: s, list(map(lambda s: convert(s), res.text.split('\n'))))
    print('get ' + str(len(list(converted))) + ' metrics')

    payload = '\n'.join(converted)

    d = requests.post('http://influxdb:8086/write?db=opentsdb', data=payload)
    print(d.text)


if __name__ == '__main__':
    while True:
        main()
        time.sleep(20)
