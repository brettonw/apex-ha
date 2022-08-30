import logging
import requests
import time
import xmltodict
from .const import *

DEFAULT_HEADERS = {"Accept": "*/*", "Content-Type": "application/json"}

_LOGGER = logging.getLogger(__name__)


class Apex(object):
    def __init__(self, username, password, deviceip):
        self.username = username
        self.password = password
        self.deviceip = deviceip
        self.sid = None
        self.version = "new"

    def auth(self):
        url = f"http://{self.deviceip}/rest/login"
        headers = {**DEFAULT_HEADERS}
        data = {"login": self.username, "password": self.password, "remember_me": False}
        _LOGGER.info(f"url ({url}), headers ({headers}), data ({data})")

        # Try logging in 3 times due to controller timeout
        login = 0
        while login < 3:
            r = requests.post(url, headers=headers, json=data)
            _LOGGER.debug(r.text)
            _LOGGER.debug(r.status_code)
            # _LOGGER.debug(r.text)
            # _LOGGER.debug(r.request.body)

            if r.status_code == 200:
                result = r.json()
                self.sid = result["connect.sid"]
                return True
            if r.status_code == 404:
                self.version = "old"
                return True
            login += 1
        return False

    def oldstatus(self):
        # Function for returning information on old controllers (Currently not authenticated)
        r = requests.get(f"http://{self.deviceip}/cgi-bin/status.xml?{str(round(time.time()))}", headers={**DEFAULT_HEADERS})
        xml = xmltodict.parse(r.text)
        # Code to convert old style to new style json
        result = {}
        system = {}
        system["software"] = xml[STATUS]["@software"]
        system["hardware"] = xml[STATUS]["@hardware"] + " Legacy Version (Status.xml)"

        result["system"] = system

        inputs = []
        for value in xml[STATUS]["probes"]["probe"]:
            inputdata = {}
            inputdata[DID] = "base_" + value[NAME]
            inputdata[NAME] = value[NAME]
            inputdata[TYPE] = value[TYPE]
            inputdata["value"] = value["value"]
            inputs.append(inputdata)

        result[INPUTS] = inputs

        outputs = []
        for value in xml[STATUS]["outlets"][ApexEntityType.OUTLET]:
            _LOGGER.debug(value)
            outputdata = {}
            outputdata[DID] = value["deviceID"]
            outputdata[NAME] = value[NAME]
            outputdata[STATUS] = [value["state"], "", "OK", ""]
            outputdata["id"] = value["outputID"]
            outputdata[TYPE] = ApexEntityType.OUTLET
            outputs.append(outputdata)

        result[OUTPUTS] = outputs

        _LOGGER.debug(result)
        return result

    def status(self):
        _LOGGER.debug(self.sid)
        if self.sid is None:
            _LOGGER.debug("We are none")
            self.auth()

        if self.version == "old":
            result = self.oldstatus()
            return result
        i = 0
        while i <= 3:
            headers = {**DEFAULT_HEADERS, f"Cookie": "connect.sid={self.sid}"}
            r = requests.get(f"http://{self.deviceip}/rest/status?_={str(round(time.time()))}", headers=headers)
            # _LOGGER.debug(r.text)

            if r.status_code == 200:
                return r.json()
            elif r.status_code == 401:
                self.auth()
            else:
                _LOGGER.debug("Unknown error occurred")
                return {}
            i += 1

    def config(self):
        if self.version == "old":
            return {}
        if self.sid is None:
            _LOGGER.debug("We are none")
            self.auth()

        headers = {**DEFAULT_HEADERS, f"Cookie": "connect.sid={self.sid}"}
        r = requests.get(f"http://{self.deviceip}/rest/config?_={str(round(time.time()))}", headers=headers)
        # _LOGGER.debug(r.text)

        if r.status_code == 200:
            return r.json()

        print("Error occured")

    def toggle_output(self, did, state):
        """
        XXX I'm giving the TYPE: OUTLET a bit of side-eye, as it should be the type of the output
        entity, but this seems to work without having to find the output type in the status.
        """
        data = {DID: did, STATUS: [state, "", "OK", ""], TYPE: ApexEntityType.OUTLET}
        _LOGGER.debug(data)

        headers = {**DEFAULT_HEADERS, f"Cookie": "connect.sid={self.sid}"}
        r = requests.put(f"http://{self.deviceip}/rest/status/outputs/{did}", headers=headers, json=data)
        data = r.json()
        _LOGGER.debug(data)

        return data

    def set_variable(self, did, code):

        config = self.config()

        # find the variable in the output configuration
        variable = None
        for output in config[OUTPUT_CONFIG]:
            if output[DID] == did:
                variable = output
        if variable is None:
            return {"error": f"Variable '{did}' not found"}

        """
        'ctype' is the Apex template for the program they embed. 'Advanced' is a bare program. if we
        are setting a variable, we want to take control of that value, so the Apex templates are not
        useful. it's useful to issue a warning if we are changing that type, but not necessary to
        retain it.
        """
        if variable[CTYPE] != ADVANCED:
            _LOGGER.warning(f"Changing variable '{did}' {CTYPE} to '{ADVANCED}' from '{variable[CTYPE]}' with prog='{variable[PROG]}'")
            variable[CTYPE] = ADVANCED

        variable[PROG] = code
        _LOGGER.debug(variable)

        headers = {**DEFAULT_HEADERS, f"Cookie": "connect.sid={self.sid}"}
        r = requests.put(f"http://{self.deviceip}/rest/config/oconf/{did}", headers=headers, json=variable)

        _LOGGER.debug(r.text)

        return {"error": ""}
