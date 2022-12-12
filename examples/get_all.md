## Usage example
# COMAP Smart Home public API example

## Retrieve all data for all housings

```python
from comapsmarthome_public_api.client_auth import ClientAuth
from comapsmarthome_public_api.comap_obj import HousingsState

comap_username = 'yourcomapuser'
comap_password = 'yourcomappassword'


def main():
    auth = ClientAuth(username=comap_username,
                      password=comap_password)

    hstate = HousingsState(auth)

    for kh, housing in hstate.housings.items():
        print(housing)
        for kz, zone in housing.zones.items():
            print(zone)
        print("\nload_thermal_details")
        print("====================\n")
        hstate.load_thermal_details(kh)
        for kz, zone in housing.zones.items():
            print("\n\n{}\n".format(zone))
            for khard, hardware in zone.hardwares.items():
                print(hardware)


if __name__ == '__main__':
    main()
```
