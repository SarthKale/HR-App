import os
from xml.etree import ElementTree
from mysql.connector import connect, Error
from datetime import datetime

"""
It is the Data Layer of the HRApplication, in this we access
and perform CRUD operations directly to the tables in the Database.
The Database consists of 2 Tables of use for this application and
in this module, we configure and validate the connections between MySQL
and data-layer.
In this, we transfer data between DBMS and data-layer by the means
of class objects.
In this, the configuration details are to be provided by the user in
the form of an XML file(the demo XML file is given by the name of
'dbconfig.xml')
"""


class DataLayerError(Exception):
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


class DBUtility:
    """
    A class that contains the method to parse the user provided
    configuration file and extracts the necessary data as well as
    validates it.
    """
    def getDBConfiguration():
        """
        It parses the user-provided configuration file along with
        validating it.

        Exception Raising:
            raises DataLayerError exception.

        Return Value:
            returns DBConfiguration object with the data provided by the user
            in the configuration file.
        """
        if not os.path.isfile("dbconfig.xml"):
            raise DataLayerError(
                message="'dbconfig.xml' file not found, please refer documentation")
        f = open("dbconfig.xml", "rt")
        try:
            xmlTree = ElementTree.parse(f)
        except ElementTree.ParseError:
            raise DataLayerError(
                "dbconfig.xml is malformed, refer documentation.")
        finally:
            f.close()
        rootNode = xmlTree.getroot()
        host = port = database = user = password = None
        for node in rootNode:
            if node.tag == 'host':
                host = node.text
            if node.tag == 'port':
                port = node.text
            if node.tag == 'name':
                database = node.text
            if node.tag == 'user':
                user = node.text
            if node.tag == 'password':
                password = node.text
        if port != None:
            try:
                int(port)
            except:
                raise DataLayerError(
                    message=f"Port is of type {type(port)}, it should be of type {type(0)}")
        return DBConfiguration(host, int(port), database, user, password)


class Designation:
    """
    A class that creates an object which holds all the necessary entries
    for the Designation Table of the Database.
    It allows performing CRUD operations on Designation Table directly by
    connecting to the MySQL database.

    Attributes:
        code(int): It holds the code entry of the Designation Table in the
        Database.
        title(str): It holds the designation title entry of the Designation
        Table in the Database.

    Methods:
        _validate_values:
            validates the entries in Designation class and
            accumulates all the exceptions into the exceptions
            variable. Also toggles has_exceptions variable accordingly.
    """

    def __init__(self, code, title):
        self.exceptions = dict()
        self.has_exceptions = False
        self.code = code
        self.title = title
        self._validate_values()

    def _validate_values(self):
        """
        _validate_values:
            validates the entries in Designation class and accumulates
            all the exceptions into the exceptions' variable.
            Also toggles has_exceptions variable accordingly.

            Exception Raising:
                raises DataLayerError exception.
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
                    'V', f"Value of title is {len(self.title)}, it should be greater than zero and less than 35")
        if len(self.exceptions) > 0:
            self.has_exceptions = True


class Employee:
    """
    A class that creates an object which holds all the necessary entries
    for the Employee Table of the Database.
    It allows performing CRUD operations on Employee Talbe directly by
    connecting to the MySQL database.

    Attributes:
        _designation_codes_register(dict): the dictionary that holds
        all the designation code entries from the Designation table
        allowing only those values to be allocated to the Employee Table.

        emp_id(int): the employee ID entry for the Employee Table in
        Database.
        name(str): the employee name entry for the Employee Table in
        Database.
        designation_code(int): the designation code of employee for
        the Employee Table in Database.
        date(int): the date part of Date of Birth entry for Employee
        Table in Database.
        month(int): the month part of Date of Birth entry for Employee
        Table in Database.
        year(int): the year part of Date of Birth entry for Employee
        Table in Database.
        salary(float): the employee salary entry for the Employee Table
        in Database.
        gender(str): the employee gender entry for Employee Table in
        Database.
        indian(int): the employee is_indian entry for Employee Table
        in Database.
        pan_no(str): the employee pan_number entry for Employee Table
        in Database.
        aadhar(str): the employee aadhar_number entry for Employee
        Table in Database.
        dob(datetime.datetime): the employee Date_of_Birth entry for
        Employee Table in Database.
            default is None(NoneType)
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
            variable of the Employee class. It also toggles
            the has_exceptions variable accordingly.

        _populate_register:
            stores the values of all the available designation codes
            from Designation Table into the _designation_codes_register
            variable.
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
        Employee._populate_register()
        self._validate_values()
        if not self.has_exceptions:
            self.dob = datetime(self.year, self.month,
                                self.date).strftime("%Y-%m-%d")

    def _populate_register():
        """
        Stores the values of all the available designation codes
        from Designation Table into the _designation_codes_register
        variable.

        Raise Exception:
            raises DataLayerError when can't call the get_designations
            method of HRDLHandler
        """
        try:
            designations = HRDLHandler.get_designations()
            for designation in designations:
                Employee._designation_codes_register[designation.code] = designation
        except DataLayerError as dle:
            print(dle.message)
            print(dle.exceptions)

    def _validate_values(self):
        """
        _validate_values:
            validates the entries in Employee class and accumulates
            all the exceptions into the exceptions' variable.
            Also toggles has_exceptions variable accordingly.

            Exception Raising:
                raises DataLayerError exception.
        """
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


class DBConfiguration:
    """
    A class that validates the configuration information that
    the DBUtility class' getDBConfiguration returns.

    Attributes:
        host(str): the host address of the Database connection with
        the system.
        port(int): the port address of the Database connection that
        is 3306.
        database(str): the name of the database.
        user(str): the username of the database connection which is
        to be provided by the user.
        password(str): the password of database connection which is
        to be provided by the user.

    Methods:
        _validate_values:
            validates the entries in DBConfiguration class and
            accumulates all the exceptions into the exceptions
            variable of the Employee class. Also toggles
            has_exceptions variable accordingly.
            Exception Raising:
                raises DataLayerError exception.
    """

    def __init__(self, host, port, database, user, password):
        self.exceptions = dict()
        self.has_exceptions = False
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self._validate_values()

    def _validate_values(self):
        """
        _validate_values:
            validates the entries in DBConfiguration class and
            accumulates all the exceptions into the exceptions' variable.
            Also toggles has_exceptions variable accordingly.

            Exception Raising:
                raises DataLayerError exception.
        """
        if isinstance(self.host, str) == False:
            self.exceptions["host"] = (
                'T', f"host is of type {type(self.host)}, it should be of type {type('A')}")
        if isinstance(self.port, int) == False:
            self.exceptions["port"] = (
                'T', f"port is of type {type(self.port)}, it should be of type {type(10)}")
        if isinstance(self.database, str) == False:
            self.exceptions["database"] = (
                'T', f"database is of type {type(self.database)}, it should be of type {type('A')}")
        if isinstance(self.user, str) == False:
            self.exceptions["user"] = (
                'T', f"user is of type {type(self.user)}, it should be of type {type('A')}")
        if isinstance(self.password, str) == False:
            self.exceptions["password"] = (
                'T', f"password is of type {type(self.password)}, it should be of type {type('A')}")
        if 'host' not in self.exceptions and len(self.host) == 0:
            self.exceptions["host"] = ('V', "host ip/name is missing")
        if 'port' not in self.exceptions and (self.port <= 0 or self.port >= 65535):
            self.exceptions['port'] = (
                'V', "port is not in the permissible range, unable to assign.")
        if 'database' not in self.exceptions and len(self.database) == 0:
            self.exceptions["database"] = ('V', "database name is missing")
        if 'user' not in self.exceptions and len(self.user) == 0:
            self.exceptions["user"] = ('V', "user is missing")
        if 'password' not in self.exceptions and len(self.password) == 0:
            self.exceptions["password"] = ('V', "password is missing")
        if len(self.exceptions) > 0:
            self.has_exceptions = True


class DBConnection:
    """
    A class that sets the connection between the database whose details
    are provided by the user and this module.

    Methods:
        getConnection:
            this method utilizes the data returned by DBUtility class'
            getDBConfiguration method and sets the connection between
            the database and the module.
    """
    def getConnection():
        """
        It utilizes the data returned by DBUtility class'
        getDBConfiguration method and sets the connection between
        the database and the module.

        Exception Raising:
            raises DataLayerError exception.
        """
        dbConfig = DBUtility.getDBConfiguration()
        if dbConfig.has_exceptions:
            raise DataLayerError(exceptions=dbConfig.exceptions)
        try:
            connection = connect(host=dbConfig.host, port=dbConfig.port,
                                 database=dbConfig.database, user=dbConfig.user, password=dbConfig.password)
        except Error as error:
            raise DataLayerError(message=error.msg)
        return connection


class HRDLHandler:
    """
    A class which consist of all the methods that perform
    CRUD operation on the database, specifically to the
    Designation and the Employee tables.

    Methods:
        add_designation: adding a new designation entry to
        the Designation Table.
        add_employee: adding a new employee entry to
        the Employee Table.
        update_designation: updates a designation entry to
        the Designation Table.
        update_employee: updates an employee entry to
        the Employee Table.
        delete_designation: removes an existing designation entry in
        the Designation Table.
        delete_employee: removes an existing employee entry in
        the Employee Table.
        get_designations: retrieves all the entries from the Designation
        Table.
        get_employees: retrieves all the entries from the Employee Table.
        get_designation_by_code: retrieves a entry from the Designation
        Table that has the specific designation code given by the user.
        get_employee_by_id: retrieves an entry from the Employee Table
        that has the specific employee ID given by the user.
        get_designation_by_title: retrieves a entry from the Designation
        Table that has the specific designation title given by the user.
        get_employee_by_name: retrieves all the entries from the Employee Table
        that has the specific employee's name given by the user.
        get_designation_count: retrieves the number, the total of entries
        present in the Designation Table.
        get_employee_count: retrieves the number, the total of entries
        present in the Employee Table.
    """

    def add_designation(designation):
        """
        Adds a new entry to the Designation Table

        Exception Raising:
            raises DataLayerError exception.
        """
        if designation == None:
            raise DataLayerError(message="Designation Required")
        if not isinstance(designation, Designation):
            raise DataLayerError(
                f"Found type {type(designation)}, required type <class 'Designation'>")
        if designation.has_exceptions:
            raise DataLayerError(exceptions=designation.exceptions)
        if designation.code != 0:
            raise DataLayerError(
                "Designation Code must be assigned zero, as it is auto generated.")
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute(
                "select code from designation where title=%s", (designation.title,))
            rows = cursor.fetchall()
            if len(rows) > 0:
                raise DataLayerError(
                    message=f"{designation.title} already exists")
            cursor.execute(
                "insert into designation (title) values (%s)", (designation.title,))
            designation.code = cursor.lastrowid
            connection.commit()
        except Error as err:
            raise DataLayerError(message=err.msg)
        finally:
            try:
                if cursor.is_open():
                    cursor.close()
                if connection.is_connected():
                    connection.close()
            except:
                pass

    def add_employee(employee):
        """
        Adds a new entry to the Employee Table

        Exception Raising:
            raises DataLayerError exception.
        """
        if employee == None:
            raise DataLayerError(message="Employee Required")
        if not isinstance(employee, Employee):
            raise DataLayerError(
                f"Found type {type(employee)}, required type <class 'Employee'>")
        if employee.has_exceptions:
            raise DataLayerError(exceptions=employee.exceptions)
        if employee.emp_id != 0:
            raise DataLayerError(
                "Employee ID must be assigned zero, as it is auto generated.")
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute(
                "select emp_id from employee where name=%s", (employee.name,))
            rows = cursor.fetchall()
            cursor.execute("insert into employee (name,designation_code,DOB,salary,gender,is_indian,pan_no,aadhar_no) values (%s,%s,%s,%s,%s,%s,%s,%s)", (
                employee.name, employee.designation_code, employee.dob, employee.salary, employee.gender.capitalize(), employee.indian, employee.pan_no, employee.aadhar))
            if len(rows) > 0:
                print(
                    f"There are {len(rows) + 1} employees with same name now!")
            employee.emp_id = cursor.lastrowid
            connection.commit()
        except Error as err:
            raise DataLayerError(message=err.msg)
        finally:
            try:
                if cursor.is_open():
                    cursor.close()
                if connection.is_connected():
                    connection.close()
            except:
                pass

    def update_designation(designation):
        """
        Updates an existing entry in the Designation Table

        Exception Raising:
            raises DataLayerError exception.
        """
        if designation == None:
            raise DataLayerError(message="Designation Required")
        if not isinstance(designation, Designation):
            raise DataLayerError(
                f"Found type {type(designation)}, required type <class 'Designation'>")
        if designation.has_exceptions:
            raise DataLayerError(exceptions=designation.exceptions)
        if designation.code <= 0:
            raise DataLayerError(
                "Designation Code must not be zero, as it is the primary key.")
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute(
                "select code from designation where code=%s", (designation.code,))
            rows = cursor.fetchall()
            if len(rows) != 1:
                raise DataLayerError(
                    message=f"Code : {designation.code} does not exists")
            cursor.execute("update designation set title=%s where code=%s",
                           (designation.title, designation.code))
            cursor.execute(
                "select title from designation where code=%s", (designation.code,))
            updated_data = cursor.fetchall()
            connection.commit()
            if len(updated_data) != 1 or (updated_data[0][0] != designation.title):
                raise Error(
                    "Updation failed due to unknown interrupt, please try again")
        except Error as err:
            raise DataLayerError(message=err.msg)
        finally:
            try:
                if cursor.is_open():
                    cursor.close()
                if connection.is_connected():
                    connection.close()
            except:
                pass

    def update_employee(employee):
        """
        Updates an existing entry in the Employee Table

        Exception Raising:
            raises DataLayerError exception.
        """
        if employee == None:
            raise DataLayerError(message="Employee Required")
        if not isinstance(employee, Employee):
            raise DataLayerError(
                f"Found type {type(employee)}, required type <class 'Employee'>")
        if employee.has_exceptions:
            raise DataLayerError(exceptions=employee.exceptions)
        if employee.emp_id == 0:
            raise DataLayerError(
                "Employee ID must not be assigned zero, it must already exist.")
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute(
                "select emp_id from employee where emp_id=%s", (employee.emp_id,))
            rows = cursor.fetchall()
            if len(rows) != 1:
                raise DataLayerError(
                    message=f"{employee.emp_id} does not exists")
            cursor.execute("update employee set name=%s, designation_code=%s, DOB=%s, salary=%s, gender=%s, is_indian=%s, pan_no=%s, aadhar_no=%s where emp_id=%s", (employee.name,
                                                                                                                                                                     employee.designation_code, employee.dob, employee.salary, employee.gender.capitalize(), employee.indian, employee.pan_no, employee.aadhar, employee.emp_id))
            cursor.execute(
                "select name from employee where emp_id=%s", (employee.emp_id,))
            updated_data = cursor.fetchall()
            connection.commit()
            if len(updated_data) != 1 or (updated_data[0][0] != employee.name):
                raise Error(
                    "Updation failed due to unknown interrupt, please try again")
        except Error as err:
            raise DataLayerError(message=err.msg)
        finally:
            try:
                if cursor.is_open():
                    cursor.close()
                if connection.is_connected():
                    connection.close()
            except:
                pass

    def delete_designation(code):
        """
        Removes an existing entry from the Designation Table

        Exception Raising:
            raises DataLayerError exception.
        """
        if code == None:
            raise DataLayerError(message="Designation Code Required")
        if not isinstance(code, int):
            raise DataLayerError(
                f"Found type {type(code)}, required type {type(0)}")
        if code <= 0:
            raise DataLayerError(f"Invalid entry for code : {code}")
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute(
                "select emp_id from employee where designation_code=%s", (code,))
            rows = cursor.fetchall()
            if len(rows) != 0:
                raise DataLayerError(
                    message=f"The designation code : {code}, cannot be deleted as employees exist against it")
            cursor.execute(
                "select code from designation where code=%s", (code,))
            rows = cursor.fetchall()
            if len(rows) != 1:
                raise DataLayerError(message=f"Code : {code} does not exists")
            cursor.execute("delete from designation where code=%s", (code,))
            cursor.execute("select * from designation where code=%s", (code,))
            updated_data = cursor.fetchall()
            connection.commit()
            if len(updated_data) != 0:
                raise Error()
        except Error:
            raise DataLayerError(
                message="Deletion failed due to unknown interrupt, please try again")
        finally:
            try:
                if cursor.is_open():
                    cursor.close()
                if connection.is_connected():
                    connection.close()
            except:
                pass

    def delete_employee(emp_id):
        """
        Removes an existing entry from the Employee Table

        Exception Raising:
            raises DataLayerError exception.
        """
        if emp_id == None:
            raise DataLayerError(message="Employee ID Required")
        if not isinstance(emp_id, int):
            raise DataLayerError(
                f"Found type {type(emp_id)}, required type {type(0)}")
        if emp_id <= 0:
            raise DataLayerError(f"Invalid entry for employee ID : {emp_id}")
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute(
                "select emp_id from employee where emp_id=%s", (emp_id,))
            rows = cursor.fetchall()
            if len(rows) != 1:
                raise DataLayerError(message=f"{emp_id} does not exists")
            cursor.execute("delete from employee where emp_id=%s", (emp_id,))
            cursor.execute(
                "select emp_id from employee where emp_id=%s", (emp_id,))
            updated_data = cursor.fetchall()
            connection.commit()
            if len(updated_data) != 0:
                raise Error()
        except Error as err:
            raise DataLayerError(
                message="Deletion failed due to unknown interrupt, please try again")
        finally:
            try:
                if cursor.is_open():
                    cursor.close()
                if connection.is_connected():
                    connection.close()
            except:
                pass

    def get_designations():
        """
        Retrieves all the existing Designation entries from the
        Designation Table.

        Exception Raising:
            raises DataLayerError exception.

        Return Value: returns a list of Designation objects.
        """
        designations = list()
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("select * from designation order by code;")
            rows = cursor.fetchall()
            connection.commit()
            for data in rows:
                code, title = data
                designation = Designation(code, title)
                designations.append(designation)
        except Error as error:
            raise DataLayerError(message=error.msg)
        finally:
            try:
                if cursor.is_open():
                    cursor.close()
                if connection.is_connected():
                    connection.close()
            except:
                pass
        return designations

    def get_employees():
        """
        Retrieves all the existing Employee entries from the
        Employee Table.

        Exception Raising:
            raises DataLayerError exception.

        Return Value: returns a list of Employee objects.
        """
        employees = list()
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("select * from employee;")
            rows = cursor.fetchall()
            connection.commit()
            for data in rows:
                emp_id = data[0]
                name = data[1]
                designation_code = data[2]
                dob = data[3]
                day = dob.strftime("%d")
                month = dob.strftime("%m")
                year = dob.strftime("%Y")
                salary = data[4]
                gender = data[5]
                indian = data[6]
                pan_no = data[7]
                aadhar = data[8]
                employee = Employee(emp_id, name, designation_code, day,
                                    month, year, salary, gender, indian, pan_no, aadhar)
                employees.append(employee)
        except Error as error:
            raise DataLayerError(message=error.msg)
        finally:
            try:
                if cursor.is_open():
                    cursor.close()
                if connection.is_connected():
                    connection.close()
            except:
                pass
        return employees

    def get_designation_by_code(code):
        """
        Retrieves an existing Designation entry which matches the
        designation code value of the inputted data from the
        Designation Table.

        Attributes:
            code(int): the designation code of the desired entry.

        Exception Raising:
            raises DataLayerError exception.

        Return Value: returns a Designation class object.
        """
        if code == None:
            raise DataLayerError(message="Designation Code Required")
        if not isinstance(code, int):
            raise DataLayerError(
                f"Found type {type(code)}, required type {type(0)}")
        if code <= 0:
            raise DataLayerError(f"Invalid Code : {code}")
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("select * from designation where code=%s", (code,))
            row = cursor.fetchone()
            connection.commit()
            if row == None:
                raise DataLayerError(message=f"Code : {code} does not exists")
            code, title = row
            designation = Designation(code, title)
        except Error as error:
            raise DataLayerError(message=error.msg)
        finally:
            try:
                if cursor.is_open():
                    cursor.close()
                if connection.is_connected():
                    connection.close()
            except:
                pass
        return designation

    def get_employee_by_id(emp_id):
        """
        Retrieves an existing Employee entry which matches the
        employee ID value of the inputted data from the
        Employee Table.

        Attributes:
            emp_id(int): Employee ID of the desired Employee
            Table entry.

        Exception Raising:
            raises DataLayerError exception.

        Return Value: returns an Employee class object.
        """
        if emp_id == None:
            raise DataLayerError(message="Employee ID Required")
        if not isinstance(emp_id, int):
            raise DataLayerError(
                f"Found type {type(emp_id)}, required type {type(0)}")
        if emp_id <= 0:
            raise DataLayerError(f"Invalid employee ID : {emp_id}")
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("select * from employee where emp_id=%s", (emp_id,))
            row = cursor.fetchone()
            connection.commit()
            if row == None:
                raise DataLayerError(
                    message=f"Employee ID : {emp_id} does not exists")
            emp_id = row[0]
            name = row[1]
            designation_code = row[2]
            dob = row[3]
            day = dob.strftime("%d")
            month = dob.strftime("%m")
            year = dob.strftime("%Y")
            salary = row[4]
            gender = row[5]
            indian = row[6]
            pan_no = row[7]
            aadhar = row[8]
            employee = Employee(emp_id, name, designation_code, day,
                                month, year, salary, gender, indian, pan_no, aadhar)
        except Error as error:
            raise DataLayerError(message=error.msg)
        finally:
            try:
                if cursor.is_open():
                    cursor.close()
                if connection.is_connected():
                    connection.close()
            except:
                pass
        return employee

    def get_designation_by_title(title):
        """
        Retrieves an existing Designation entry which matches the
        designation title value of the inputted data from the
        Designation Table.

        Attributes:
            title(str): the designation title of the desired entry.

        Exception Raising:
            raises DataLayerError exception.

        Return Value: returns a Designation class object.
        """
        if title == None:
            raise DataLayerError(message="Designation Title Required")
        if not isinstance(title, str):
            raise DataLayerError(
                f"Found type {type(title)}, required type {type('A')}")
        if len(title) <= 0 or len(title) > 35:
            raise DataLayerError(
                f"The length of title exceeds max limit, it should be greater than 0 and less than 35.")
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute(
                "select * from designation where title=%s", (title,))
            row = cursor.fetchone()
            connection.commit()
            if row == None:
                raise DataLayerError(
                    message=f"Designation : {title} does not exists")
            code, title = row
            designation = Designation(code, title)
        except Error as error:
            raise DataLayerError(message=error.msg)
        finally:
            try:
                if cursor.is_open():
                    cursor.close()
                if connection.is_connected():
                    connection.close()
            except:
                pass
        return designation

    def get_employee_by_name(name):
        """
        Retrives a list of all the existing Employee entry which
        matches the employee name value of the inputed data from
        the Employee Table.

        Attributes:
            name(str): Employee name of the desired Employee
            Table entries.

        Exception Raising:
            raises DataLayerError exception.

        Return Value: returns a list of Employee class objects.
        """
        employees = list()
        if name == None:
            raise DataLayerError(message="Employee Name Required")
        if not isinstance(name, str):
            raise DataLayerError(
                f"Found type {type(name)}, required type {type('A')}")
        if len(name) <= 0 or len(name) > 35:
            raise DataLayerError(
                f"The length of name exceeds max limit, it should be greater than 0 and less than 35.")
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("select * from employee where name=%s", (name,))
            rows = cursor.fetchall()
            connection.commit()
            for data in rows:
                emp_id = data[0]
                name = data[1]
                designation_code = data[2]
                dob = data[3]
                day = dob.strftime("%d")
                month = dob.strftime("%m")
                year = dob.strftime("%Y")
                salary = data[4]
                gender = data[5]
                indian = data[6]
                pan_no = data[7]
                aadhar = data[8]
                employee = Employee(emp_id, name, designation_code, day,
                                    month, year, salary, gender, indian, pan_no, aadhar)
                employees.append(employee)
        except Error as error:
            raise DataLayerError(message=error.msg)
        finally:
            try:
                if cursor.is_open():
                    cursor.close()
                if connection.is_connected():
                    connection.close()
            except:
                pass
            return employees

    def get_designation_count():
        """
        Retrieves the value of the total number of entries present in
        the Designation Table.

        Exception Raising:
            raises DataLayerError exception.

        Return Value: returns an int equal to the total entries in
        the Designation Table.
        """
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("select count(*) as cnt from designation;")
            row = cursor.fetchone()
            connection.commit()
            count = row[0]
        except Error as error:
            raise DataLayerError(message=error.msg)
        finally:
            try:
                if cursor.is_open():
                    cursor.close()
                if connection.is_connected():
                    connection.close()
            except:
                pass
        return count

    def get_employee_count():
        """
        Retrieves the value of the total number of entries present in
        the Employee Table.

        Exception Raising:
            raises DataLayerError exception.

        Return Value: returns an int equal to the total entries in
        the Employee Table.
        """
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("select count(*) as cnt from employee;")
            row = cursor.fetchone()
            connection.commit()
            count = row[0]
        except Error as error:
            raise DataLayerError(message=error.msg)
        finally:
            try:
                if cursor.is_open():
                    cursor.close()
                if connection.is_connected():
                    connection.close()
            except:
                pass
        return count
