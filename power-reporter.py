#!/usr/bin/env python3

from prometheus_client import make_wsgi_app
from prometheus_client.core import CollectorRegistry, GaugeMetricFamily
from prometheus_client.registry import Collector
from wsgiref.simple_server import make_server
import tomllib
import tinytuya

with open('config.toml', 'rb') as f:
    config = tomllib.load(f)

class OutletMetricsCollector(Collector):
    def collect(self):
        for device in config['devices']:
            name = device['name']
            power = self._get_power_usage(
                device['device_id'],
                device['ip'],
                device['local_key'],
            )
            yield GaugeMetricFamily(f'outlet_{name}', 'Power usage of outlets (W)', power)

    def _get_power_usage(self, dev_id: str, address: str, local_key: str) -> float:
        outlet = tinytuya.OutletDevice(dev_id, address, local_key, version=3.3)
        status = outlet.status()

        match status:
            case { 'dps': {'19': cur_power} }: return cur_power / 10
            case _: raise ValueError(f'Unrecognized status: {status}')

registry = CollectorRegistry()
registry.register(OutletMetricsCollector())

metrics_port = config.get('metrics_port', 9102)

app = make_wsgi_app(registry)
httpd = make_server('0.0.0.0', metrics_port, app)
print(f'Metrics exporter listening on {httpd.server_name}:{httpd.server_port}')
httpd.serve_forever()
