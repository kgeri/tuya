#!/usr/bin/env python3

import tomllib
import tinytuya

with open('config.toml', 'rb') as f:
    config = tomllib.load(f)

for device in config['devices']:
    name = device['name']
    dev_id = device['device_id']
    address = device['ip']
    local_key=device['local_key']
    
    outlet = tinytuya.OutletDevice(dev_id, address, local_key, version=3.3)
    status = outlet.status()
    
    match status:
        case { 'dps': {'19': cur_power} }: power = cur_power / 10
        case _: raise ValueError(f'Unrecognized status: {status}')

    print(f'name={name}, ip={address}, power={power}W')
