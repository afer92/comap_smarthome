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

## Credentials

To access COMAP Smart Home product through the API, `username` and `password` need to be gived at object creation.

## Requirements

- Python >=3.6
- requests, boto3 and dateutil modules
- COMAP Smart Home user account

## Author
Petit-Pierre Melec
https://gitlab.com/melec/comapsmarthome_public_api_python
