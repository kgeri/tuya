#!/usr/bin/env python3

from prometheus_client import make_wsgi_app
from prometheus_client.core import CollectorRegistry, GaugeMetricFamily
from prometheus_client.registry import Collector
from wsgiref.simple_server import make_server
import logging
import time
import tomllib
import tinytuya


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%dT%H:%M:%SZ')
logging.Formatter.converter = time.gmtime

with open('config.toml', 'rb') as f:
    config = tomllib.load(f)

class OutletMetricsCollector(Collector):
    def collect(self):
        g = GaugeMetricFamily('power_usage_watts', 'Power usage of outlets (W)', labels=['location'])
        for device in config['devices']:
            name = device['name']
            power = self._get_power_usage(
                name,
                device['device_id'],
                device['ip'],
                device['local_key'],
            )
            g.add_metric([name], power)
        yield g

    def _get_power_usage(self, name: str, dev_id: str, address: str, local_key: str) -> float | None:
        outlet = tinytuya.OutletDevice(dev_id, address, local_key, version=3.3)
        outlet.set_socketTimeout(3)
        status = outlet.status()

        match status:
            case { 'dps': {'19': cur_power} }: return cur_power / 10
            case _:
                logging.error(f'Failed reporting {name}. Unrecognized status: {status}')
                return None

registry = CollectorRegistry()
registry.register(OutletMetricsCollector())

metrics_port = config.get('metrics_port', 9102)

app = make_wsgi_app(registry)
httpd = make_server('0.0.0.0', metrics_port, app)
logging.info(f'Metrics exporter listening on {httpd.server_name}:{httpd.server_port}')
httpd.serve_forever()
