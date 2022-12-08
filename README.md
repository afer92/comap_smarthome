# COMAP Smart Home public API

Python module to control and retrieve data for COMAP Smart Home products.

## Install

To install `comapsmarthome-prublic-api` run :

    pip install comapsmarthome-public-api
## Usage example

```python
from comapsmarthome_public_api.client_auth import ClientAuth
from comapsmarthome_public_api.measurement_service import MeasurementsService

auth = ClientAuth(username='yourcomapuser', password='yourcomappassword')
measurements = MeasurementsService(auth)

dt_from = '2020-10-01T09:30+01:00'
dt_to = '2020-10-01T10:30+01:00'
serial_number = 'aa**********'
data = measurements.get_measurements(dt_from, dt_to, serial_number=serial_number, measurements=['inside_temperature'])
dates = [d['time'] for d in data]
temperatures = [d['inside_temperature'] for d in data]
```
Other:
```python
from comapsmarthome_public_api.client_auth import ClientAuth
from comapsmarthome_public_api.comap_obj import HousingsState

def main():
    auth = ClientAuth(username='yourcomapuser', password='yourcomappassword')
    hstate = HousingsState(auth)
    for kh, housing in hstate.housings.items():
        print(housing)
        for kz, zone in housing.zones.items():
            print(zone)
        hstate.load_thermal_details(kh)
        for kz, zone in housing.zones.items():
            print("\n\n{}\n".format(zone))
            for khard, hardware in zone.hardwares.items():
                print(hardware)


if __name__ == "__main__":
    main()
```
Other:
```python
from comapsmarthome_public_api.client_auth import ClientAuth
from comapsmarthome_public_api.comap_obj import HousingsState

comap_username = 'yourcomapuser'
comap_password = 'yourcomappassword'

housing_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
zone_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

def main():
    auth = ClientAuth(username=comap_username,
                      password=comap_password)
    hstate = HousingsState(auth)
    hstate.load_thermal_details(housing_id)

    zone = hstate.get_zone_by_id(zone_id)
    print("\nZone: {}".format(zone.title))
    print("=============\n")
    line = "Consigne: {} Temperature: {} Heating: {}"
    print(line.format(zone.seted_temp, zone.temperature, zone.heating))
    print("Humidity: {}\n".format(zone.humidity))

if __name__ == "__main__":
    main()
```
## Credentials

To access COMAP Smart Home product through the API, `username` and `password` need to gived at object creation.

## Requirements

- Python >=3.6
- requests, boto3 and dateutil modules
- COMAP Smart Home user account

## Author
Petit-Pierre Melec
https://gitlab.com/melec/comapsmarthome_public_api_python