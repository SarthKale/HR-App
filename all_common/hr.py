import json
from datetime import datetime
import decimal
from data_layer.hr import HRDLHandler

"""
It is a module that connects the Network layer and the Data layer.
It creates the Designation and Employee class objects similar to
that of Data layer and transfers data to and from between Network
and Data layer in the form of JSON Strings.
"""


class ValidationError(Exception):
    """
    A class that handles the exceptions which get raised in
    Employee and Designation class.

    Attribute:
        message(str): it holds the message part of the exception.
            default is empty string("")
        exceptions(dict): it holds the cause of exceptions
        in the form of dictionary.
            default is None(NoneType)
    """

    def __init__(self, message='', exceptions=None):
        self.message = message
        self.exceptions = exceptions


class Designation:
    """
    A class which creates an object with entries present in the
    Designation Table, it is used to transfer data between
    the data layer and network layer.
    It uses JSON Strings as the data transfer format.

    Attributes:
        code(int): holds the designation code for a Designation object.
            default is 0
        title(str): holds the title value of a Designation object.
            default is empty string("")
        exceptions(dict): the dictionary which holds the exceptions
        which may occur while validating the entries of Designation object.
            default is empty dictionary({})
        has_exceptions(bool): The boolean used to determine the presence
        of exceptions in the Designation object.
            default is False

    Methods:
        _validate_values:
            validates the entries in Designation class and
            accumulates all the exceptions into the exceptions
            variable of the Designation class. Also toggles
            has_exceptions variable accordingly.

        to_json: converts the active object into a JSON String
        and returns it.

        from_json(json_string): takes a JSON string as parameter
        and converts it to a Designation object and returns this object.
        Attribute:
            json_string(JSON String Object): this string contains the parameters
            necessary to create the Designation object.
    """

    def __init__(self, code=0, title="", exceptions={}, has_exceptions=False):
        self.exceptions = dict()
        self.code = code
        self.title = title
        self.exceptions = {}
        self.has_exceptions = False
        self._validate_values()

    def _validate_values(self):
        """
        Applies all the necessary validations on the entries
        in Designation class and accumulates all the exceptions into
        the exceptions' variable of the Designation class.
        Also toggles has_exceptions variable accordingly.
        """
        if isinstance(self.code, int) == False:
            self.exceptions["code"] = (
                'T', f"code is of type {type(self.code)}, it should be of type {type(0)}")
        if isinstance(self.title, str) == False:
            self.exceptions["title"] = (
                'T', f"title is of type {type(self.title)}, it should be of type {type('A')}")
        if ('code' not in self.exceptions) and self.code < 0:
            self.exceptions["code"] = (
                'V', f"Value of code is {self.code}, it should be greater than or equal to zero")
        if "title" not in self.exceptions:
            length_of_title = len(self.title)
            if length_of_title == 0 or length_of_title > 35:
                self.exceptions["title"] = (
                    'V', f"Value of title is {self.title}, it should be greater than zero and less than 35")
        if len(self.exceptions) > 0:
            self.has_exceptions = True

    def to_json(self):
        """
        converts the active object into a JSON String.

        Return Value:
            returns the JSON String.
        """
        return json.dumps(self.__dict__, indent=4)

    def from_json(json_string):
        """
        from_json(json_string): takes a json string as parameter
        and converts it to a Designation object.
        Attribute:
            json_string(JSON String Object): this string contains all the parameters
            necessary to create the Designation object.

        Return Value:
            returns a Designation object.
        """
        new_dict = json.loads(json_string)
        return Designation(**new_dict)


class Employee:
    """
    A class which creates an object with entries present in the
    Employee Table, it is used to transfer data between
    the data layer and network layer.
    It uses JSON Strings as the data transfer format.

    Attributes:
        _designation_codes_register(dict): a dictionary to store all
        the existing designation values as Designation objects
        in Designation table, by calling the data-layer method.
        emp_id(int): holds the employee ID of the Employee object.
        name(str): holds the name of the Employee object.
        designation_code(int): holds the employee designation code
        for the Employee object.
        date(int): holds the date part of Date of Birth of the
        Employee object.
        month(int): holds the month part of Date of Birth of the
        Employee Object.
        year(int): holds the year part of Date of Birth of the
        Employee Object.
        salary(float): holds the salary of the Employee object.
        gender(str): holds the gender value of the Employee object.
            * Accepts only M/m/F/f as entries
        indian(int): holds the value of nationality of the employee in
            * Accepts only 1/0 as entries the Employee object.
        pan_no(str): holds the PAN Number of the Employee object,
        strictly of length 10.
        aadhar(str): holds the Aadhar Number of the Employee object.
        dob(datetime.datetime): holds the employee Date of Birth of
        the Employee object.
            default value is None(NoneType).
        exceptions(dict): the dictionary which holds the exceptions
        which may occur while validating the entries of Employee object.
            default is empty dictionary({})
        has_exceptions(bool): The boolean used to determine the presence
        of exceptions in the Employee object.
            default is False

    Methods:
        _validate_values:
            validates the entries in Employee class and
            accumulates all the exceptions into the exceptions
            variable of the Employee class. Also toggles
            has_exceptions variable accordingly.

        to_json: converts the active object into a JSON String
        and returns it.

        from_json(json_string): takes a json string as parameter
        and converts it to a Employee object and returns this object.
        Attribute:
            json_string(JSON String Object): this string contains the parameters
            necessary to create the Employee object.
    """

    _designation_codes_register = {}

    def __init__(self, emp_id, name, designation_code, date, month, year, salary, gender, indian, pan_no, aadhar, dob=None, exceptions={}, has_exceptions=False):
        self.exceptions = exceptions
        self.has_exceptions = has_exceptions
        self.emp_id = emp_id
        self.name = name
        self.designation_code = designation_code
        self.date = date
        self.month = month
        self.year = year
        self.salary = salary
        self.gender = gender
        self.indian = indian
        self.pan_no = pan_no
        self.aadhar = aadhar
        self.dob = dob
        self._validate_values()
        if not self.has_exceptions:
            self.dob = datetime(self.year, self.month,
                                self.date).strftime("%Y-%m-%d")

    def _validate_values(self):
        """
        Applies all the necessary validations on the entries
        in Employee class and accumulates all the exceptions into
        the exceptions' variable of the Exception class.
        Also toggles has_exceptions variable accordingly.
        """
        designations = HRDLHandler.get_designations()
        for designation in designations:
            Employee._designation_codes_register[designation.code] = designation

        if not isinstance(self.emp_id, int):
            self.exceptions["emp_id"] = (
                'T', f"employee id is of type {type(self.emp_id)}, it should be of type {type(0)}")
        if not isinstance(self.name, str):
            self.exceptions["name"] = (
                'T', f"name is of type {type(self.name)}, it should be of type {type('A')}")
        if not isinstance(self.designation_code, int):
            self.exceptions["designation_code"] = (
                'T', f"designation_code is of type {type(self.designation_code)}, it should be of type {type(0)}")
        if not isinstance(self.date, int):
            self.exceptions["dob"] = (
                'T', f"date is of type {type(self.date)}, it should be of type {type(0)}")
        if not isinstance(self.month, int):
            self.exceptions["dob"] = (
                'T', f"month is of type {type(self.month)}, it should be of type {type(0)}")
        if not isinstance(self.year, int):
            self.exceptions["dob"] = (
                'T', f"year is of type {type(self.year)}, it should be of type {type(0)}")
        if not isinstance(self.salary, float):
            self.exceptions["salary"] = (
                'T', f"salary is of type {type(self.salary)}, it should be of type {type(10.2)}")
        if not isinstance(self.gender, str):
            self.exceptions["gender"] = (
                'T', f"gender is of type {type(self.gender)}, it should be of type {type('A')}")
        if not isinstance(self.indian, int):
            self.exceptions["indian"] = (
                'T', f"indian is of type {type(self.indian)}, it should be of type {type(0)}")
        if not isinstance(self.pan_no, str):
            self.exceptions["pan_no"] = (
                'T', f"PAN number is of type {type(self.pan_no)}, it should be of type {type('A')}")
        if not isinstance(self.aadhar, str):
            self.exceptions["aadhar"] = (
                'T', f"Aadhar number is of type {type(self.aadhar)}, it should be of type {type('A')}")

        if ('emp_id' not in self.exceptions) and self.emp_id < 0:
            self.exceptions["emp_id"] = (
                'V', f"Value of emp_id is {self.emp_id}, it should be greater than or equal to zero")
        if "name" not in self.exceptions:
            length_of_name = len(self.name)
            if length_of_name == 0 or length_of_name > 35:
                self.exceptions["name"] = (
                    'V', f"Value of name is {self.name}, it should be greater than zero and less than 35")
        if ("designation_code" not in self.exceptions) and (self.designation_code not in Employee._designation_codes_register):
            self.exceptions["designation_code"] = (
                'V', f"Invalid Designation Code : {self.designation_code}")
        if ("dob" not in self.exceptions):
            if self.date <= 0 or self.date > 31:
                self.exceptions["dob"] = (
                    'V', f"Invalid Date entry : {self.date}, it should be greater than zero and should not exceed 31")
            if self.month <= 0 or self.month > 12:
                self.exceptions["dob"] = (
                    'V', f"Invalid Month entry : {self.month}, it should be greater than zero and should not exceed 12")
            if self.year <= 1950 or self.year > 2020:
                self.exceptions["dob"] = (
                    'V', f"Invalid Year entry : {self.year}, it should be greater than 1950 and should not exceed 2020")
        if ("salary" not in self.exceptions) and self.salary <= 0:
            self.exceptions["salary"] = (
                'V', f"Invalid Entry for Basic Salary")
        if ("gender" not in self.exceptions) and (self.gender not in 'MmFf' or len(self.gender) != 1):
            self.exceptions["gender"] = ('V', f"Invalid entry for gender")
        if ("indian" not in self.exceptions) and (self.indian not in [0, 1]):
            self.exceptions["indian"] = ('V', f"Invalid entry for indian")
        if ("pan_no" not in self.exceptions) and (len(self.pan_no) != 10):
            self.exceptions["pan_no"] = ('V', f"Invalid entry for Pan Number")
        if ("aadhar" not in self.exceptions) and (len(self.aadhar) != 10):
            self.exceptions["aadhar"] = (
                'V', f"Invalid entry for Aadhar Number")
        if len(self.exceptions) > 0:
            self.has_exceptions = True
        if len(self.exceptions) > 0:
            self.has_exceptions = True

    def to_json(self):
        """
        converts the active object into a JSON String.

        Return Value:
            returns the JSON String.
        """
        print(type(self))
        print(self.__dict__)
        if isinstance(self.salary, decimal.Decimal):
            self.salary = float(self.salary)
        return json.dumps(self.__dict__, indent=4)

    def from_json(json_string):
        """
        from_json(json_string): takes a JSON string as parameter
        and converts it to an Employee object.
        Attribute:
            json_string(JSON String Object): this string contains all the parameters
            necessary to create the Employee object.

        Return Value:
            returns the Employee object.
        """
        new_dict = json.loads(json_string)
        return Employee(**new_dict)
