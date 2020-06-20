from homeassistant.core import callback
from homeassistant.helpers.entity import Entity


import logging
import asyncio
import requests
import json

from datetime import timedelta

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = []

SCAN_INTERVAL = timedelta(minutes=30)

cookie = '__RequestVerificationToken=m5YHWkYuk0ae5bdmH9teGMeM5mXzsJDOcFiCqmwBmG1MsvJIaHdaoXm7sRp7sgXFfk1T9QEVic0SccLwG6f4UGNsiePDPIMIjlfmZ0rd7dk1;'






@asyncio.coroutine
def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    swiftcommand = SwiftCommand(hass, config)
    async_add_entities([swiftcommand], True)
    return True

class SwiftCommand(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass, config):
        """Initialize the sensor."""
        self._state = None
        self._email = config.get("email")
        self._password = config.get("password")
        self._assetid = config.get("assetid")
        self._formdata = {'Email': self._email,
                'Password': self._password,
                '__RequestVerificationToken': '0Vz0de7tVuXAeCqanchIILRrKDdbAWezSMUceAEFpRl9fPDp0aoj2FY88Ejmq7K74svUwSRlmJyhE9kFWbTYVHjIe4JIEgq5cYb1KStF2Uo1',
                'RememberMe': 'false'}
        
        self._attributes = {}
        _LOGGER.warning("Setting up SwiftCommand")

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'SwiftCommand'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "v"

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return self._attributes

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        login_headers = { 'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': f'https://swiftcommand.azurewebsites.net/Vans__/CustomerSingleVehicleMap/{self._assetid}',
                'Cookie': cookie}


        update_headers = {'content-type': 'application/json',
            'Referer': f'https://swiftcommand.azurewebsites.net/Vans__/CustomerSingleVehicleMap/{self._assetid}'}

        session = requests.Session()

        login = session.post(f'https://swiftcommand.azurewebsites.net/Account/Login?ReturnUrl=%2FVans__%2FCustomerVehicleDetails%2F{self._assetid}',
                        headers=login_headers, data=self._formdata)


        r = session.get(f'https://swiftcommand.azurewebsites.net/api/Mapping/GetLastDataVehiclePoint/?AssetID={self._assetid}&_=1592511317003', headers=update_headers)

        if "log in" in r.text:
            print("Not logged in")
            self._state = "Login error"
        else:
            data = r.json()
            lastData = data["lastData"]
            vehicle = data["Vehicle"]
            loc_lat = lastData["Lat"]/1000000
            loc_long = lastData["Long"]/1000000
            loc_time = lastData["FixtimeLocal"]
            voltage_unit = f"{lastData['LeisureVoltage']/10}v"
            temp_c = f"{round((lastData['Temp'] - 32) * 5/9, 2)}°c"
            voltage = lastData["LeisureVoltage"]/10
            # temp = (lastData["Temp"] − 32) * 5/9
            Van_Serial_Number = vehicle["Van_Serial_Number"]
            make = vehicle["Make"]
            model = vehicle["Model"]
            attribs = {"latitude": loc_lat, "longitude": loc_long, "time": loc_time, "voltage": voltage_unit, "temp": temp_c, "van_serial": Van_Serial_Number, "make": make, "model": model, "entity_picture": "/local/caravan.jpg"}
            self._attributes = attribs
            self._state = voltage
