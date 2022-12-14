#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comapsmarthome_public_api.client_auth import ClientAuth
from comapsmarthome_public_api.measurement_service import MeasurementsService
from comapsmarthome_public_api.park_service_client import ParkServiceClient
from comapsmarthome_public_api.thermal_service import ThermalService
from comapsmarthome_public_api.comap_obj_static import *
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


class Housing(Housing_static):

    def __init__(self, data, hstate):
        super().__init__(data)
        self._hstate = hstate


class Zone(Zone_static):

    def __init__(self, housing, data, hstate):
        super().__init__(housing, data)
        self._hstate = hstate

    def test_thermal_details(self):
        if self._last_transmission is None:
            self._hstate.load_thermal_details(self._housing.id)
        if self._last_transmission is not None:
            self._last_transmission_age = self.date_age(self._last_transmission)
        if self._last_transmission_age > 10:
            self._hstate.load_thermal_details(self._housing.id)
            self._last_transmission_age = self.date_age(self._last_transmission)


class Hardware(Hardware_static):

    def __init__(self, zone, data):
        super().__init__(zone, data)


class HousingsState(comap_obj):

    def __init__(self, auth):

        def add_hardware(self, zone_obj, hardware_id):
            hardware_infos = self._park.get_connected_object(hardware_id)
            hard_obj = Hardware(zone_obj, hardware_infos)
            zone_obj._hardwares[hardware_infos["serial_number"]] = hard_obj

        def add_zone(housing_obj, zone_id, hstate):
            zone_obj = Zone(housing_obj, zone_id, hstate)
            housing_obj.add_zone(zone_obj)
            for o_connected in zone_obj._connected_objects:
                add_hardware(self, zone_obj, o_connected)

        self._auth = auth
        self._park = ParkServiceClient(auth)
        self._ts = ThermalService(auth)
        self._housings = self._park.get_housings()
        self._obj_housings = {}

        for housing_data in self._housings:
            housing_obj = Housing(housing_data, self)
            self._obj_housings[housing_obj.id] = housing_obj
            zones = self._ts.get_zones(housing_obj.id)
            for zone_id in zones:
                add_zone(housing_obj, zone_id, self)
            gct = self._ts.get_custom_temperatures
            housing_obj._custom_temperatures = gct(housing_obj.id)

    def load_thermal_details(self, housingId):
        housing = self._obj_housings[housingId]
        zones = housing.zones
        td = self._ts.get_housing_thermal_details(housingId)
        housing.set_thermal_details(td)

    def get_hardware_by_serial(self, serial):
        for kho, housing in self._obj_housings.items():
            for kz, zone in housing._zones.items():
                for kha, hardware in zone._hardwares.items():
                    if hardware.serial_number == serial:
                        return hardware
        return None

    def get_zone_by_id(self, id):
        for kho, housing in self._obj_housings.items():
            for kz, zone in housing._zones.items():
                if zone.id == id:
                    return zone
        return None

    @property
    def housings(self):
        return self._obj_housings
        
