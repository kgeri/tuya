#!/usr/bin/env python3

from prometheus_client import make_wsgi_app
from prometheus_client.core import CollectorRegistry, GaugeMetricFamily
from prometheus_client.registry import Collector
from PyNUTClient import PyNUT
from wsgiref.simple_server import make_server
import logging
import time
import tinytuya
import tomllib


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
        OutletMetricsCollector._report_tuya_devices(g)
        OutletMetricsCollector._report_nut_devices(g)
        yield g

    @staticmethod
    def _report_tuya_devices(g: GaugeMetricFamily):
        for device in config.get('tuya_device', []):
            name = device['name']
            power = OutletMetricsCollector._get_tuya_power_usage(
                name,
                device['device_id'],
                device['ip'],
                device['local_key'],
            )
            if power: g.add_metric([name], power)

    @staticmethod
    def _get_tuya_power_usage(name: str, dev_id: str, address: str, local_key: str) -> float | None:
        outlet = tinytuya.OutletDevice(dev_id, address, local_key, version=3.3)
        outlet.set_socketTimeout(3)
        status = outlet.status()

        match status:
            case { 'dps': {'19': cur_power} }: return cur_power / 10
            case _:
                logging.error(f'Failed reporting {name}. Unrecognized status: {status}')
                return None
    
    @staticmethod
    def _report_nut_devices(g: GaugeMetricFamily):
        for device in config.get('nut_device', []):
            name = device['name']

            nut = PyNUT.PyNUTClient(host = device['ip'], port = device.get('port', 3493))
            vars = nut.GetUPSVars(device['device_id'])
            power = float(vars[b'ups.realpower'].decode('utf-8'))
            g.add_metric([name], power)

registry = CollectorRegistry()
registry.register(OutletMetricsCollector())

metrics_port = config.get('metrics_port', 9102)

app = make_wsgi_app(registry)
httpd = make_server('0.0.0.0', metrics_port, app)
logging.info(f'Metrics exporter listening on {httpd.server_name}:{httpd.server_port}')
httpd.serve_forever()
