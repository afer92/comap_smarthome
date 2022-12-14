#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.tz import *


class comap_obj:

    def __init__(self):
        pass

    @staticmethod
    def strdate2date(data):
        dtformat = '%Y-%m-%dT%H:%M:%S%z'
        timestamp = data[:19] + data[26:].replace(":", "")
        return datetime.strptime(timestamp, dtformat)

    @staticmethod
    def date_age(dt2compute):
        delta = datetime.now(tzlocal()) - dt2compute
        age = int(delta.seconds / 60)
        return age


class Housing_static(comap_obj):

    def __init__(self, data):
        self._data = data
        self._id = data['id']
        self._hstate = None
        self._user_id = data['user_id']
        self._name = data['name']
        self._address = data['address']
        self._zip_code = data['zip_code']
        self._city = data['city']
        self._country = data['country']
        self._longitude = data['longitude']
        self._latitude = data['latitude']
        self._type = data['type']
        self._usage = data['usage']
        self._ip_address = data['ip_address']
        self._created_at = self.strdate2date(data['created_at'])
        self._timezone = data['timezone']
        self._connected_objects = data['connected_objects']
        self._custom_temperatures = None
        self._heating_system_state = None
        self._services_available = None
        self._events = None
        self._zones = {}
        self._meters_registered = None

    def __str__(self):
        line1 = "Housing {} created {}\nid: {} user_id: {}\n"
        line2 = "address: {} {} {} {}\n"
        line3 = "coord. gps: {},{}\n"
        line4 = "type: {} usage :{}\n"
        line5 = "{} connected objects\n"
        part = line1.format(self._name, self._created_at,
                            self._id, self._user_id)
        part += line2.format(self._address, self._zip_code,
                             self._city, self._country)
        part += line3.format(self._latitude, self._longitude)
        part += line4.format(self._type, self._usage)
        part += line5.format(len(self._connected_objects))
        for oneobject in self._connected_objects:
            part += "\tserial: {}\n".format(oneobject)
        return part

    def add_zone(self, zone):
        self._zones[zone.id] = zone

    def set_thermal_details(self, data):
        self._heating_system_state = data["heating_system_state"]
        self._services_available = data["services_available"]
        self._events = data["events"]
        self._meters_registered = data["meters_registered"]
        zones = data["zones"]
        for zone in zones:
            self._zones[zone["id"]].set_thermal_details(zone)

    @property
    def id(self):
        return self._id

    @property
    def user_id(self):
        return self._user_id

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def zip_code(self):
        return self._zip_code

    @property
    def city(self):
        return self._city

    @property
    def country(self):
        return self._country

    @property
    def longitude(self):
        return self._longitude

    @property
    def latitude(self):
        return self._latitude

    @property
    def h_type(self):
        return self._type

    @property
    def usage(self):
        return self._usage

    @property
    def ip_address(self):
        return self._ip_address

    @property
    def created_at(self):
        return self._created_at

    @property
    def timezone(self):
        return self._timezone

    @property
    def connected_objects(self):
        return self._connected_objects

    @property
    def zones(self):
        return self._zones

    @property
    def last_transmission(self):
        return self._last_transmission


class Zone_static(comap_obj):

    def __init__(self, housing, data):
        self._housing = housing
        self._data = data
        self._id = data['id']
        self._title = data['title']
        self._area_type = data['area_type']
        if 'instruction_type' in data.keys():
            self._instruction_type = data['instruction_type']
        else:
           self._instruction_type = None
        if 'heating_priority' in data.keys():
            self._heating_priority = data['heating_priority']
        else:
           self._heating_priority = None
        if 'services_available' in data.keys():
            self._services_available = data['services_available']
        else:
           self._services_available = None
        if 'connected_objects' in data.keys():
            self._connected_objects = data['connected_objects']
        else:
           self._connected_objects = None
        self._open_window = None
        self._last_transmission = None
        self._last_transmission_age = None
        self._transmission_error = None
        self._temperature = None
        self._humidity = None
        self._programming_type = None
        self._set_point_type = None
        self._set_point = None
        self._next_timeslot = None
        self._heating_status = None
        self._events = None
        self._last_presence_detected = None
        self._errors = None
        self._hardwares = {}

    def __str__(self):
        line1 = "Zone {} Type {} id: {}\n"
        line2 = "Instruction type: {} Heating priority: {}\n"
        line3 = "Service available: {}\n"
        line5 = "{} connected objects\n"
        part = line1.format(self._title, self._area_type,
                            self._id)
        part += line2.format(self._instruction_type, self._heating_priority)
        part += line3.format(self._services_available)
        if self._connected_objects is not None:
            part += line5.format(len(self._connected_objects))
            for oneobject in self._connected_objects:
                part += "\tserial: {}\n".format(oneobject)
                if self._last_transmission is not None:
                    part += self.print_thermal_details()
        for hk, hardware in self.hardwares.items():
            part += "\n{}".format(hardware)
        return part

    def test_thermal_details(self):
        pass

    def set_thermal_details(self, data):
        self._transmission_error = data['transmission_error']
        self._last_transmission = self.strdate2date(data['last_transmission'])
        self._errors = data['errors']
        if data['transmission_error']:
            return
        self._open_window = data['open_window']
        self._temperature = data['temperature']
        self._humidity = data['humidity']
        self._programming_type = data['programming_type']
        self._set_point_type = data['set_point_type']
        self._set_point = data['set_point']
        self._next_timeslot = data['next_timeslot']
        self._heating_status = data['heating_status']
        self._events = data['events']
        self._last_presence_detected = self.strdate2date(data['last_presence_detected'])

    def print_thermal_details(self):
        line1 = "  Temperature: {} Humidity: {} Last transmission: {}\n"
        line1a = "  Seted temperature: {} Heating: {}\n"
        line2 = "  Programming type: {}, Set point type: {}\n"
        line3 = "  Heating status: {}, Next time slot: {}\n"
        line4 = "  Last presence detected: {}\n"
        part = line1.format(self._temperature, self._humidity,
                            self._transmission_error)
        part += line1a.format(self.seted_temp, self.heating)
        part += line2.format(self._programming_type, self._set_point_type)
        part += line3.format(self._heating_status,
                             self._next_timeslot["begin_at"])
        part += "  Instruction: {}\n".format(self._next_timeslot["set_point"])
        spi = self._next_timeslot["set_point"]["instruction"]
        if spi in self._housing._custom_temperatures.keys():
            cust = self._housing._custom_temperatures[spi]
            part += "  Next set point: {}°C".format(cust)
        elif spi in self._housing._custom_temperatures["connected"]:
            cust = self._housing._custom_temperatures["connected"][spi]
            part += "  Next set point: {}°C".format(cust)
        part += line4.format(self._last_presence_detected)
        if self._open_window:
            part += "  Window open"
        for error in self._errors:
            part += "  {}".format(error)
        for event in self._events:
            part += "  {}".format(event)
        return part

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def area_type(self):
        return self._area_type

    @property
    def instruction_type(self):
        return self._instruction_type

    @property
    def heating_priority(self):
        return self._heating_priority

    @property
    def services_available(self):
        return self._services_available

    @property
    def connected_objects(self):
        return self._connected_objects

    @property
    def set_point(self):
        self.test_thermal_details()
        return self._set_point

    @property
    def temperature(self):
        self.test_thermal_details()
        return self._temperature

    @property
    def humidity(self):
        self.test_thermal_details()
        return self._humidity

    @property
    def seted_temp(self):
        self.test_thermal_details()
        if self._last_transmission is not None:
            spi = self._set_point["instruction"]
            if self._set_point_type == 'defined_temperature':
                if spi in self._housing._custom_temperatures.keys():
                    return self._housing._custom_temperatures[spi]
                elif spi in self._housing._custom_temperatures["connected"]:
                    return self._housing._custom_temperatures["connected"][spi]
            elif self._set_point_type == 'custom_temperature':
                return spi
            else:
                return None
        else:
            return None

    @property
    def housing(self):
        return self._housing

    @property
    def hardwares(self):
        return self._hardwares

    @property
    def heating(self):
        self.test_thermal_details()
        return (self._heating_status == "heating")

    @property
    def last_transmission(self):
        self.test_thermal_details()
        return self._last_transmission

    @property
    def last_presence_detected(self):
        self.test_thermal_details()
        return self._last_presence_detected

    @property
    def last_transmission_age(self):
        self.test_thermal_details()
        return self._last_transmission_age

    @property
    def zone_summary(self):
        result = ""
        line = "\nZone: {}\n".format(self._title)
        result += line
        line = "=" * (len(self._title) + 6) + "\n\n"
        result += line
        line = "Last transmission: {} ({}mn)\n"
        line = line.format(self._last_transmission,
                           self._last_transmission_age)
        result += line
        line = "Consigne: {} Temperature: {} Heating: {}\n"
        line = line.format(self.seted_temp,
                           self.temperature,
                           self.heating)
        result += line
        line = "Humidity: {}\n"
        line = line.format(self.humidity)
        result += line
        return result


class Hardware_static(comap_obj):

    def __init__(self, zone, data):
        self._data = data
        self._zone = zone
        self._serial_number = data['serial_number']
        self._housing_id = data['housing_id']
        self._model = data['model']
        self._last_communication_time = self.strdate2date(data['last_communication_time'])
        self._first_communication_time = self.strdate2date(data['first_communication_time'])
        self._is_new = data['is_new']
        self._firmware_version = data['firmware_version']
        if self._model == "thermostat":
            self._voltage = data['voltage']
            self._voltage_percent = data['voltage_percent']
            self._last_temperature = data['last_temperature']
        else:
            self._voltage = None
            self._voltage_percent = None
            self._last_temperature = None

        if self._model == "heating_module":
            self._is_blinking = data['is_blinking']
        else:
            self._is_blinking = None

    def __str__(self):
        line1 = "Serial number: {} Model: {}\n"
        line2 = "First communication time: {}\n"
        line3 = "Last communication time: {}\n"
        line4 = "Is new: {}, Firmware version: {}\n"
        part = line1.format(self._serial_number, self._model)
        part += line2.format(self._first_communication_time)
        part += line3.format(self._last_communication_time)
        part += line4.format(self._is_new, self._firmware_version)
        if self._model == "thermostat":
            line5 = "Voltage: {} {}%, Last temperature: {}\n"
            part += line5.format(self._voltage,
                                 self._voltage_percent,
                                 self._last_temperature)
        if self._model == "heating_module":
            line5 = "Is blinking: {}\n"
            part += line5.format(self._is_blinking)
        return part

    @property
    def serial_number(self):
        return self._serial_number

    @property
    def housing_id(self):
        return self._housing_id

    @property
    def model(self):
        return self._model

    @property
    def last_communication_time(self):
        return self._last_communication_time

    @property
    def first_communication_time(self):
        return self._first_communication_time

    @property
    def is_new(self):
        return self._is_new

    @property
    def firmware_version(self):
        return self._firmware_version

    @property
    def voltage(self):
        return self._voltage

    @property
    def voltage_percent(self):
        return self._voltage_percent

    @property
    def last_temperature(self):
        return self._last_temperature

    @property
    def is_blinking(self):
        return self._is_blinking
        

def main():
    housing_id = 'aaaaaaaa-bbbb-5555-5555-cccccccccccc'
    user_id = '6aaaaaaa-bbbb-5555-5555-cccccccccccc'
    connected_objects = ['aa2345678901', 'bb1234567890', 'bb2345678901', 'aa1234567890', '1c1234567890']
    
    hgs_data = {'id': housing_id,
                  'user_id': user_id,
                  'name': 'My house',
                  'address': '99 Main Street',
                  'zip_code': '12LH123',
                  'city': 'Mycity',
                  'country': 'uk',
                  'longitude': 2.14,
                  'latitude': 48.89,
                  'type': 'apartment',
                  'usage': 'main',
                  'ip_address': '11.22.33.44',
                  'created_at': '2021-12-22T13:13:09.960475+00:00',
                  'timezone': 'Europe/London',
                  'connected_objects': connected_objects,
                  'upgrade_parameters': {'version': None, 'installation_type': None, 'installation_mode': None}}
    housing = Housing_static(hgs_data)
    print(housing)

    zon_data = {'id': '655dc360-d661-4917-acc8-3b64d413d246',
                'title': 'Chambre',
                'area_type': 'bedroom',
                'instruction_type': 'temperature',
                'heating_priority': 'secondary',
                'services_available': True,
                'connected_objects': [connected_objects[3], connected_objects[1]]}
    zone = Zone_static(housing, zon_data)
    print(zone)

    housing.add_zone(zone)
    for kz, zone in housing.zones.items():
        print(kz, "\n", zone)

    hwa_data = {'serial_number': connected_objects[3],
                'housing_id': housing_id,
                'model': 'thermostat',
                'last_communication_time': '2022-12-13T17:37:18.778773+00:00',
                'first_communication_time': '2021-12-22T15:03:10.497659+00:00',
                'voltage': 3.79,
                'voltage_percent': 39,
                'is_new': False,
                'firmware_version': 1143,
                'last_temperature': 19.59,
                'errors': [], 
                'temporary_commands': []}
    hardware = Hardware_static(zone, hwa_data)
    print(hardware)

    hwa_data = {'serial_number': connected_objects[1],
                'housing_id': housing_id,
                'model': 'heating_module',
                'last_communication_time': '2022-12-13T17:39:48.729865+00:00',
                'first_communication_time': '2021-12-22T15:02:14.026053+00:00',
                'is_new': False, 'firmware_version': 2118,
                'is_blinking': False, 'errors': [], 'temporary_commands': []}
    hardware2 = Hardware_static(zone, hwa_data)

    zone._hardwares[hardware.serial_number] = hardware
    zone._hardwares[hardware2.serial_number] = hardware2
    
    print(zone)

if __name__ == "__main__":
    main()
