#!/usr/bin/env python3

import argparse
import sys
import tinytuya

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--address', '-a', help='the IP address of the socket')
parser.add_argument('--devid', '-d', help='the Device ID')
parser.add_argument('--key', '-k', help='the Local Key of the device')
args = parser.parse_args()

device = tinytuya.OutletDevice(
    dev_id=args.devid,
    address=args.address,
    local_key=args.key,
    version=3.3,
)

status = device.status()
print(status['dps'])
