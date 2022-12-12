## Usage example
# COMAP Smart Home public API example

## Retrieve zone by id

```python
from comapsmarthome_public_api.client_auth import ClientAuth
from comapsmarthome_public_api.comap_obj import HousingsState

comap_username = 'yourcomapuser'
comap_password = 'yourcomappassword'


def zone_infos(hstate, zone_id):
    # get zone by id
    zone = hstate.get_zone_by_id(zone_id)
	# dump data
    print("\nZone: {}".format(zone.title))
    line = "=" * (len(zone.title) + 6)
    print(line, "\n")
    line = "Last transmission: {} ({}mn)"
    print(line.format(zone.last_transmission,
                      zone.last_transmission_age))
    line = "Consigne: {} Temperature: {} Heating: {}"
    print(line.format(zone.seted_temp, zone.temperature, zone.heating))
    print("Humidity: {}\n".format(zone.humidity))


def main():
    auth = ClientAuth(username=comap_username,
                      password=comap_password)

    hstate = HousingsState(auth)

    for kh, housing in hstate.housings.items():
        print(housing)
        for zone_id, zone in housing.zones.items():
            zone_infos(hstate, zone_id)


if __name__ == '__main__':
    main()
```
Same result:
```python
from comapsmarthome_public_api.client_auth import ClientAuth
from comapsmarthome_public_api.comap_obj import HousingsState

comap_username = 'yourcomapuser'
comap_password = 'yourcomappassword'


def zone_infos(hstate, zone_id):
    # get zone by id
    zone = hstate.get_zone_by_id(zone_id)
	# dump data
    print(zone.zone_summary)


def main():
    auth = ClientAuth(username=comap_username,
                      password=comap_password)

    hstate = HousingsState(auth)

    for kh, housing in hstate.housings.items():
        print(housing)
        for zone_id, zone in housing.zones.items():
            zone_infos(hstate, zone_id)


if __name__ == '__main__':
    main()
```

