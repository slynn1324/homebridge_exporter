# Homekit (Homebridge) Prometheus Textfile Collector

## Running

```
usage: homebridge_exporter.py [-h] [--output OUTPUT] --address ADDRESS --port
                           PORT --pin PIN
homebridge_exporter.py: error: the following arguments are required: --address, --port, --pin
```

```
python3 homebridge_exporter.py --address xxx.xxx.xxx.xxx --port 51826 --pin xxx-xx-xxx
```

## Depends On

Leverages https://github.com/mrstegeman/hapclient