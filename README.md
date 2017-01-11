# opentsdb-metrics-to-influxdb
[![](https://img.shields.io/travis/wyvernnot/opentsdb-metrics-to-influxdb.svg)](https://travis-ci.org/wyvernnot/opentsdb-metrics-to-influxdb)

Import opentsdb metrics to influxdb

### Environment Variable

|            |   |
|------------|---|
|OPENTSDB_URL| http://opentsdb:4246/api/stats  |
|INFLUXDB_URL| http://influxdb:8086/write?db=opentsdb  |
|INTERVAL    | 10   |

### Usage

```
docker run wyvernnot/opentsdb-metrics-to-influxdb
```

