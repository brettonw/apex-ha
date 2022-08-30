import logging
import requests
import time
from .const import *
from typing import Optional

DEFAULT_HEADERS = {"Accept": "*/*", "Content-Type": "application/json"}

_LOGGER = logging.getLogger(__name__)


class Apex(object):
    def __init__(
            self, username, password, deviceip
    ):

        self.username = username
        self.password = password
        self.deviceip = deviceip
        self.sid = None
        self.version = "new"

    def auth(self):
        data = {
            "login": self.username,
            "password": self.password,
            "remember_me": False
        }
        # Try logging in 3 times due to controller timeout
        login = 0
        while login < 3:
            r = requests.post("http://" + self.deviceip + "/rest/login", headers=DEFAULT_HEADERS, json=data)

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
            else:
                print("Status code failure")
                login += 1
        return False

    def status(self):
        _LOGGER.debug(self.sid)
        if self.sid is None:
            _LOGGER.debug("We are none")
            self.auth()

        i = 0
        while i <= 3:
            headers = {**DEFAULT_HEADERS, f"Cookie": "connect.sid={self.sid}"}
            r = requests.get("http://" + self.deviceip + "/rest/status?_=" + str(round(time.time())), headers=headers)
            # _LOGGER.debug(r.text)

            if r.status_code == 200:
                result = r.json()
                return result
            elif r.status_code == 401:
                self.auth()
            else:
                _LOGGER.debug(f"Unknown error occurred {r.status_code}, {r.reason}")
                return {}
            i += 1

    def config(self):
        if self.sid is None:
            _LOGGER.debug("We are none")
            self.auth()
        headers = {
            **DEFAULT_HEADERS,
            "Cookie": "connect.sid=" + self.sid
        }

        r = requests.get("http://" + self.deviceip + "/rest/config?_=" + str(round(time.time())), headers=headers)
        # _LOGGER.debug(r.text)

        if r.status_code == 200:
            result = r.json()
            return result
        else:
            print("Error occured")

    def toggle_output(self, did, state):
        headers = {**DEFAULT_HEADERS, f"Cookie": "connect.sid={self.sid}"}

        """
        XXX giving the TYPE: OUTLET a bit of side-eye, as it should be the type of the output
        entity, but this seems to work without having to find the output type in the status.
        """
        data = {DID: did, STATUS: [state, "", "OK", ""], TYPE: ApexEntityType.OUTLET}
        _LOGGER.debug(data)

        r = requests.put(f"http://{self.deviceip}/rest/status/outputs/{did}", headers=headers, json=data)
        data = r.json()
        _LOGGER.debug(data)

        return data

    def set_variable(self, did, set_value: Optional[int], set_code: Optional[str]) -> dict:
        headers = {**DEFAULT_HEADERS, f"Cookie": "connect.sid={self.sid}"}

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

        if (set_code is None) and (set_value is None):
            _LOGGER.warning(f"set_variable '{did}' called with no 'code' or 'value', ignoring")
        else:
            # at least one of the two inputs (set_value, set_code) is valid, maybe both.
            # if set_code is not valid, take the set_value
            if set_code is None:
                set_code = f"Set {set_value}\n"

            # save out the program
            variable[PROG] = set_code
            _LOGGER.debug(variable)

            r = requests.put(f"http://{self.deviceip}/rest/config/oconf/{did}", headers=headers, json=variable)
            _LOGGER.debug(r.text)

        return {"error": ""}
