# Tuya IoT integrations

## Hardware prep (iGET Power 4 USB)

```
pipx install tonytuya
tinytuya scan
```

Follow https://github.com/jasonacox/tinytuya#setup-wizard---getting-local-keys.
Roughly:

* Register on https://iot.tuya.com/
* Create a new project, "Development Method" must be "Smart Home"
* Install the "Tuya Smart" app on mobile, do the pairing with the devices (iGET is Tuya-compatible)
* Add "IoT Core" and "Authorization Token Management" to Service API
* "Devices" / "Link App Account", scan the QA code from the mobile app, and sync devices automatically
* Run `cd .tuyaconfig && tinytuya wizard`, and specify:
  * The "Access ID/Client ID"
  * The "Access Secret/Client Secret"
  * Have it scan the network, it'll find the devices and download their details from their server (including the "Local Key")

## Project setup

See https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-a-new-virtual-environment

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

```
cp config.sample.toml config.toml
# Add the ids and keys to the config
```

# iGET Documentation

Response returned by `tinytuya`, and what it means:

|**Key**|**Value**      |**Description**                                                    |
|-------|---------------|-------------------------------------------------------------------|
| 1     | switch_1      | on/off state of the first socket (counting from the power button) |
| 2     | switch_2      | on/off state of the second socket                                 |
| 3     | switch_3      | on/off state of the third socket                                  |
| 4     | switch_4      | on/off state of the fourth socket                                 |
| 7     | switch_usb1   | on/off state of the USB hub                                       |
| 9-15  | countdown_*   | time left (seconds?) until switchoff for 1-4 and usb              |
| 18    | cur_current   | current, 0-30000 mA                                               |
| 19    | cur_power     | power, 0-50000 W (scale=1, so has to be divided by 10)            |
| 20    | cur_voltage   | voltage, 0-5000 V (scale=1, so has to be divided by 10)           |
| 26    | ???           | ???                                                               |
| 38    | relay_status  | default state after power outage: 0=power_off, 1=power_on, 2=last |
| 41    | cycle_time    | ???                                                               |
| 42    | random_time   | ???                                                               |

# Links

* https://github.com/home-assistant/core/blob/dev/homeassistant/components/tuya/sensor.py
