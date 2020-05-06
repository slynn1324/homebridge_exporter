# Homekit (Homebridge) Prometheus Textfile Collector

A node_exporter textfile collector script to extract information from homebridge connected devices and make available to prometheus.

TODO: convert to an typical prometheus exporter

## Setup
```
cd hapclient
pip3 install .
```

## Running

```
usage: homebridge_exporter.py [-h] [--output OUTPUT] --address ADDRESS --port
                           PORT --pin PIN
homebridge_exporter.py: error: the following arguments are required: --address, --port, --pin
```

```
python3 homebridge_exporter.py --address xxx.xxx.xxx.xxx --port 51826 --pin xxx-xx-xxx --output /path/to/homebridge.prom
```

## Depends On

Leverages https://github.com/mrstegeman/hapclient
