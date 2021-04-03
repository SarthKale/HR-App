import json
from all_common.hr import Designation, Employee
import decimal
from sk_components.components import Wrapper

"""
A module that automates the data transfer between
the server and the client in the form of JSON Strings.
"""


class Request:
    """
    A class whose object works as a requesting object in the Network Layer.

    Attributes:
        manager(str): specifies the Menu object from which the request
        is generated.
        action(str): specifies the type of request made.
        request_object(Request): the object that is to be sent as a
        request to the Network Layer.
            default value is None(NoneType)

    Methods:
        to_json: converts the active Request object into a JSON String.
        from_json: converts the given JSON String into it's corresponding
        class type object.
    """

    def __init__(self, manager, action, request_object=None):
        self.manager = manager
        self.action = action
        if request_object != None and (isinstance(request_object, str) == False):
            self.json_string = request_object.to_json()
        else:
            self.json_string = "{}"

    def to_json(self):
        """
        It converts the active Request object into a JSON String.

        Return Value: return a JSON String.
        """
        return json.dumps(self.__dict__, indent=4)

    def from_json(json_string):
        """
        converts the given JSON String into its corresponding Request
        object.

        Attributes:
            json_string(str): the JSON String that is to be converted.

        Return Value: return a Request class object.
        """
        new_dict = json.loads(json_string)
        r = Request(new_dict["manager"], new_dict["action"], None)
        r.json_string = new_dict["json_string"]
        return r


class Response:
    """
    A class that works as a response object in the Network Layer.

    Attributes:
        success(bool): specifies a successful response from the
        Server's side is generated.
        error: specifies the errors occurred at the Server-side
        while processing the request.
            default value is None(NoneType)
        result_object(Response): the object that is to be received as a
        response by the Client Side/User.
            default value is None(NoneType)

    Methods:
        to_json: converts the active Response object into a JSON String.
        from_json: converts the given JSON String into it's corresponding
        class type object.
    """

    def __init__(self, success, error=None, result_obj=None):
        self.success = success
        if error != None:
            self.error_json = error.to_json()
        else:
            self.error_json = "{}"
        if result_obj != None:
            self.result_json = result_obj.to_json()
        else:
            self.result_json = "{}"

    def to_json(self):
        """
        converts the active Response object into a JSON String.

        Return Value: returns a JSON String.
        """
        return json.dumps(self.__dict__, indent=4)

    def from_json(json_string):
        """
        converts the given JSON String into its corresponding Response
        object.

        Attributes:
            json_string(str): the JSON String that is to be converted.

        Return Value: returns a Response class object.
        """
        new_dict = json.loads(json_string)
        r = Response(new_dict["success"])
        r.error_json = new_dict["error_json"]
        r.result_json = new_dict["result_json"]
        return r


class ExceptionHandler(Exception):
    """
    A class that converts the raised custom Exceptions into JSON String
    and vise-versa.

    Attributes:
        message(str): message part of the custom exception
        exceptions(dict): exception part of the custom exception

    Method:
        to_json: converts the active ExceptionHandler object into a JSON String.
        from_json: converts the given JSON String into it's corresponding
        custom exception.
    """

    def __init__(self, message="", exceptions=None):
        self.message = message
        self.exceptions = exceptions

    def to_json(self):
        """
        converts the active ExceptionHandler object into a JSON String.

        Return Value: returns a JSON String.
        """
        return json.dumps(self.__dict__, indent=4)

    def from_json(json_string):
        """
        converts the given JSON String into it's corresponding
        custom exception.

        Attributes:
            json_string(str): the JSON String that is to be converted.

        Return Value: returns a custom exception class.
        """
        new_dict = json.loads(json_string)
        e = ExceptionHandler(**new_dict)
        return e


def object_converter(self):
    """
    makes the class object JSON Serializable.
    """
    if isinstance(self, decimal.Decimal):
        self = float(self)
        return Wrapper(self).__dict__
    return self.__dict__


class ListHandler:
    """
    A class that converts the given list object into JSON String
    and vise-versa.

    Attributes:
        lst(list): the list type object that is to be manipulated.

    Method:
        to_json: converts the active ListHandler object into a JSON String.
        from_json: converts the given JSON String into it's corresponding
        list type object.
    """

    def __init__(self, lst):
        self.name = type(lst[0]).__name__
        self.lst = lst
        print(self.name)
        print(self.lst)

    def to_json(self):
        """
        converts the active ListHandler object into a JSON String.

        Return Value: return a JSON String.
        """
        return json.dumps(self, indent=4, default=object_converter)

    def from_json(json_string):
        """
        converts the given JSON String into it's corresponding
        list type object.

        Attributes:
            json_string(str): the JSON String that is to be converted.

        Return Value: return a list.
        """
        new_dict = json.loads(json_string)
        name = new_dict["name"]
        l1 = list(map(lambda dictionary: eval(
            f"{name}(**{dictionary})"), new_dict["lst"]))
        return l1
