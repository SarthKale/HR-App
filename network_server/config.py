import json
import sys
import os


class Configuration:
    """
    A class that configures the sockets with the system
    and validates the connectivity between server and client.
    It needs a serverconf.cfg which consist of the port number in the JSON format.
    Example:
        {port: port_number(int)}

    Attributes:
        _obj(NoneType): this is an object initialized to make the class
        a Singleton class which holds the data about configuration.

        Attributes:
            host(str): This holds the host data of the connection
            that is to be established between server and client.
            port(int): This holds the port number of the connection
            where the server socket is to be connected.
            has_exceptions(bool): The flag used to determine the presence
            of exceptions that may have raised while trying to establish the connection.
                (default value is False)
            exceptions(dict): The dictionary that holds the record of all the
            exceptions present in the connection data that is processed
            from the file provided by the user/client.

    Methods:
        _validate_values:
            Validates the connectivity data(host and port details)
            of the connection to ensure a secure and smooth connection
            and flow of data.
    """
    _obj = None

    def __new__(cls):
        """
        Initializes the _obj variable and returns it.
        The data of connection are read from a custom file provided by the user/client
        by the name of 'serverconf.cfg' in which host and port data are provided.
        """
        if Configuration._obj is not None:
            return Configuration._obj
        if not os.path.isfile("network_server/serverconf.cfg"):
            print("Configuration file missing, refer documentation")
            sys.exit()
        try:
            with open("network_server/serverconf.cfg") as json_file:
                new_dict = json.load(json_file)
        except json.decoder.JSONDecodeError:
            print("Contents of serverconf.cfg is not of JSON type, refer documentation.")
            sys.exit()
        Configuration._obj = super(Configuration, cls).__new__(cls)
        Configuration._obj.port = None
        Configuration._obj.has_exceptions = False
        Configuration._obj.exceptions = dict()
        if "port" in new_dict:
            Configuration._obj.port = new_dict["port"]

        return Configuration._obj

    def _validate_values(self):
        """
        It validates the _obj object's attributes as per the needs
        for a stable and secure connection.
        It accumulates all the possible errors present in the connection data
        and also toggles the value of has_exception
        depending on the presence of exceptions.
        """
        if Configuration._obj.port is None:
            Configuration._obj.exceptions["port"] = (
                'V', "port entry is missing in serverconf.cfg, refer documentation")
        elif not isinstance(Configuration._obj.port, int):
            Configuration._obj.exceptions["port"] = (
                'T', f"Port is of type {type(Configuration._obj.port)}, should be of type {type(10)}")
        elif Configuration._obj.port < 1024 or Configuration._obj.port > 49151:
            Configuration._obj.exceptions["port"] = (
                'V', f"Port Value is {Configuration._obj.port}, it should be within Range(1024,49151)")
        if len(Configuration._obj.exceptions) > 0:
            Configuration._obj.has_exceptions = True
