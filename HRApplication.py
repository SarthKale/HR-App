import sys
import json
from sk_components.components import Menu, Wrapper
from network_client.client import NetworkClient
from network_common.wrappers import Request, Response, ExceptionHandler, ListHandler
from all_common.hr import Designation, Employee, ValidationError


def main_menu_handler(menu, choice):
    """
    This module handles the main menu options according to the user's choice.
    It calls the activate method for the corresponding menu to make it active
    or deactivates the main menu to quit the application.
    It has three options:
    First to navigate to the Designation Menu,
    Second to navigate to the Employee Menu,
    The third is to quit the application.

    Arguments:
        menu (Menu class object): The menu object responsible for the main menu of the application.
        choice (int): The user's choice is to be handled.
    """
    if choice == 1:
        designation_menu.activate()
    if choice == 2:
        employee_menu.activate()
    if choice == 3:
        menu.deactivate()


def designation_menu_handler(menu, choice):
    """
    Handles the Designation Menu Options according to the user choice
    and calls the appropriate methods of the HRClientUI class(refer to HRClient docstring).
    Has seven options;
    first is to add a new designation to the Designation Table,
    second is to edit one of the existing designations present in the Designation Table,
    third is to delete an existing designation from the Designation Table,
    forth is to retrieve a designation by its code number,
    fifth is to retrieve a designation by its designation title,
    sixth is to retrieve all the designations currently present in the Designation Table,
    seventh is to return to the Main Menu.
    Arguments:
        menu (Menu class object): The menu object responsible for Designation Menu of the Application.
        choice (int): The user choice that is to be handled.
    Returns:
        None: a NoneType object.
    """
    if choice == 1:
        hr_client_ui = HRClientUI()
        hr_client_ui.add_designation()

    if choice == 2:
        hr_client_ui = HRClientUI()
        hr_client_ui.update_designation()

    if choice == 3:
        hr_client_ui = HRClientUI()
        hr_client_ui.remove_designation()

    if choice == 4:
        hr_client_ui = HRClientUI()
        hr_client_ui.search_designation_by_code()

    if choice == 5:
        hr_client_ui = HRClientUI()
        hr_client_ui.search_designation_by_title()

    if choice == 6:
        hr_client_ui = HRClientUI()
        hr_client_ui.get_all_designations()

    if choice == 7:
        menu.deactivate()


def employee_menu_handler(menu, choice):
    """
    Handles the Employee Menu Options according to the user choice
    and calls the appropriate methods of the HRClientUI class(refer to HRClient docstring).
    Has seven options;
    first is to add a new employee data to the Employee Table,
    second is to edit one of the existing employees' data present in the Employee Table,
    third is to delete an existing employee's data from the Employee Table,
    forth is to retrieve an employee's data by its employee ID,
    fifth is to retrieve an employee's data by his/her name,
    sixth is to retrieve all the employees' data currently present in the Employee Table,
    seventh is to return to the Main Menu.

    Arguments:
        menu (Menu class object): The menu object responsible for Employee Menu of the Application.
        choice (int): The user choice that is to be handled.

    Returns:
        None: a NoneType object.
    """
    if choice == 1:
        hr_client_ui = HRClientUI()
        hr_client_ui.add_employee()

    if choice == 2:
        hr_client_ui = HRClientUI()
        hr_client_ui.update_employee()

    if choice == 3:
        hr_client_ui = HRClientUI()
        hr_client_ui.remove_employee()

    if choice == 4:
        hr_client_ui = HRClientUI()
        hr_client_ui.search_employee_by_id()

    if choice == 5:
        hr_client_ui = HRClientUI()
        hr_client_ui.search_by_name()

    if choice == 6:
        hr_client_ui = HRClientUI()
        hr_client_ui.get_all_employees()

    if choice == 7:
        menu.deactivate()


class HRClientUI:
    """
    Utilize the network facility within this module as the to connect to the data layer
    by using the multithreaded server and requesting it by the client object
    and to perform the CRUD operations according to the user's choice.

    Methods:
        add_designation:
            adds a new designation to the Designation Table
            by taking the designation title as input at runtime.

        update_designation:
            edits any of the existing designations to the Designation Table
            by taking the designation code and title as input at runtime.

        remove_designation:
            deletes one of the existing designations in the Designation Table
            by taking the designation code as input at runtime.

        get_all_designations:
            retrieves all the available designation entries and displays them.

        search_designation_by_code:
            retrieves the desired designation by taking designation code
            as input at runtime.

        search_designation_by_title:
            retrieves the desired designation by taking designation title
            as input at runtime.

        add_employee:
            adds a new employee's data to the Employee Table
            by taking the employee's required data as input at runtime.

        update_employee:
            edits any of the existing employee's data to the Employee Table
            by taking the employee's required data as input at runtime.

        remove_employee:
            deletes one of the existing employee data in the Employee Table
            by taking the employee ID as input at runtime.

        get_all_employees:
            retrieves all the available employee entries and displays them.

        search_employee_by_id:
            retrieves the desired employee data by taking employee id
            as input at runtime.

        search_employee_by_name:
            retrieves all the desired employees' data by taking employee's name as input at runtime.
    """

    def __init__(self):
        pass

    def add_designation(self):
        """
        adds a new designation to the Designation Table
        by taking the designation title as input at runtime
        and creating a Designation class object.
        Creates a request class object,
        sends it using the NetworkClient class object and receives a response class object.
        This response object is then processed and prints the data sent in the response.
        """
        title = input("Enter the Designation to add : ")
        designation = Designation(0, title)
        request = Request(manager="DesignationManager",
                          action="add", request_object=designation)
        network_client = NetworkClient()
        response = network_client.send(request)
        if response.success:
            print("Designation Added")
        else:
            er = ExceptionHandler.from_json(response.error_json)
            if er.exceptions is None:
                print(er.message)
            else:
                for exception in er.exceptions.values():
                    print(exception[1])
        print("-" * 50)

    def add_employee(self):
        """
        adds a new employee's data to the Employee Table
        by taking the employee's required data as input at runtime
        and creating an Employee object.
        Creates a request class object,
        sends it using the NetworkClient class object and receives a response class object.
        This response object is then processed and prints the data sent in the response.
        """
        try:
            name = None
            designation_code = None
            date = None
            month = None
            year = None
            salary = None
            gender = None
            indian = None
            pan_no = None
            aadhar = None
            name = input("Enter Name of the Employee : ")
            designation_code = int(
                input("Enter the Designation Number of the Employee : "))
            date = int(input("Enter the Date : "))
            month = int(input("Enter the Month : "))
            year = int(input("Enter the Year : "))
            salary = float(input("Enter the Salary of the Employee : "))
            gender = input("Enter the Gender of the Employee : ")
            indian = int(input("Enter 1 for Indian otherwise enter 0 : "))
            pan_no = input("Enter the PAN Number of the employee : ")
            aadhar = input("Enter the Aadhar Number of the employee : ")
            employee = Employee(0, name, designation_code, date,
                                month, year, salary, gender, indian, pan_no, aadhar)
            request = Request(manager="EmployeeManager",
                              action="add", request_object=employee)
            network_client = NetworkClient()
            response = network_client.send(request)
            if response.success:
                print("Employee Added")
            else:
                er = ExceptionHandler.from_json(response.error_json)
                if er.exceptions is None:
                    print(er.message)
                else:
                    for exception in er.exceptions.values():
                        print(exception[1])
        except:
            print(f"Invalid entry type for fields of employee information form!")
        print("-" * 50)

    def update_designation(self):
        """
        edits any of the existing designations to the Designation Table
        by taking the designation code and title as input at runtime
        and creating a Designation class object.
        Creates a request class object,
        sends it using the NetworkClient class object and receives a response class object.
        This response object is then processed and prints the data sent in the response.
        """
        try:
            code = int(input("Enter the Designation Code : "))
            title = input("Enter the Designation Name : ")
            designation = Designation(code, title)
            request = Request(manager="DesignationManager",
                              action="update", request_object=designation)
            network_client = NetworkClient()
            response = network_client.send(request)
            if response.success:
                print("Designation Update")
            else:
                er = ExceptionHandler.from_json(response.error_json)
                if er.exceptions is None:
                    print(er.message)
                else:
                    for exception in er.exceptions.values():
                        print(exception[1])
        except:
            print("Invalid entry type for fields of employee information form!")
        print("-" * 50)

    def update_employee(self):
        """
        edits any of the existing employee's data to the Employee Table
        by taking the employee's required data as an input at runtime,
        and creating an Employee class object.
        Creates a request class object,
        sends it using the NetworkClient class object and recieves a response class object.
        This response object is than processed and prints the data sent in the response.
        """
        try:
            emp_id = int(input("Enter the Employee ID : "))
            name = input("Enter Name of the Employee : ")
            designation_code = int(
                input("Enter the Designation Number of the Employee : "))
            date = int(input("Enter the Date : "))
            month = int(input("Enter the Month : "))
            year = int(input("Enter the Year : "))
            salary = float(input("Enter the Salary of the Employee : "))
            gender = input("Enter the Gender of the Employee : ")
            indian = int(input("Enter 1 for Indian otherwise enter 0 : "))
            pan_no = input("Enter the PAN Number of the employee : ")
            aadhar = input("Enter the Aadhar Number of the employee : ")
            employee = Employee(emp_id, name, designation_code, date,
                                month, year, salary, gender, indian, pan_no, aadhar)
            request = Request(manager="EmployeeManager",
                              action="update", request_object=employee)
            network_client = NetworkClient()
            response = network_client.send(request)
            if response.success:
                print("Employee Updated")
            else:
                er = ExceptionHandler.from_json(response.error_json)
                if er.exceptions is None:
                    print(er.message)
                else:
                    for exception in er.exceptions.values():
                        print(exception[1])
        except:
            print("Invalid entry type for fields of employee information form!")
        print("-" * 50)

    def remove_designation(self):
        """
        deletes one of the existing designations in the Designation Table
        by taking the designation code as input at runtime
        and sending it via a Wrapper class object to the request class object.
        Creates a request class object,
        sends it using the NetworkClient class object and receives a response class object.
        This response object is then processed and prints the data sent in the response.
        """
        try:
            code = int(input("Enter the Designation Code : "))
            request = Request(manager="DesignationManager",
                              action="remove", request_object=Wrapper(code))
            network_client = NetworkClient()
            response = network_client.send(request)
            if response.success:
                print("Designation Deleted")
            else:
                er = ExceptionHandler.from_json(response.error_json)
                if er.exceptions is None:
                    print(er.message)
                else:
                    for exception in er.exceptions.values():
                        print(exception[1])
        except:
            print(
                f"code is of unexpected type, it should be of type {type(0)}")
        print("-" * 50)

    def remove_employee(self):
        """
        deletes one of the existing employee data in the Employee Table
        by taking the employee ID as input at runtime,
        and sending it via a Wrapper class object to the request class object.
        Creates a request class object,
        sends it using the NetworkClient class object and receives a response class object.
        This response object is then processed and prints the data sent in the response.
        """
        try:
            emp_id = int(input("Enter the Employee ID : "))
            request = Request(manager="EmployeeManager",
                              action="remove", request_object=Wrapper(emp_id))
            network_client = NetworkClient()
            response = network_client.send(request)
            if response.success:
                print("Employee Deleted")
            else:
                er = ExceptionHandler.from_json(response.error_json)
                if er.exceptions is None:
                    print(er.message)
                else:
                    for exception in er.exceptions.values():
                        print(exception[1])
        except:
            print(
                f"employee id is of unexpected type, it should be of type {type(0)}")
        print("-" * 50)

    def get_all_designations(self):
        """
        Retrieves all the available designation entries and displays them.
        Creates a request class object,
        sends it using the NetworkClient class object and receives a response class object.
        This response object is then processed and prints the data sent in the response
        in the form of a list.
        """
        request = Request(manager="DesignationManager", action="getall")
        network_client = NetworkClient()
        response = network_client.send(request)
        if response.success:
            designations = ListHandler.from_json(response.result_json)
            for designation in designations:
                print(
                    f"Code : {designation.code} Designation : {designation.title}")
        else:
            er = ExceptionHandler.from_json(response.error_json)
            if er.exceptions is None:
                print(er.message)
            else:
                for exception in er.exceptions.values():
                    print(exception[1])
        print("-" * 50)

    def get_all_employees(self):
        """
        Retrieves all the available employee entries and displays them.
        Creates a request class object,
        sends it using the NetworkClient class object and receives a response class object.
        This response object is then processed and prints the data sent in the response
        in the form of a list.
        """
        request = Request(manager="EmployeeManager", action="getall")
        network_client = NetworkClient()
        response = network_client.send(request)
        if response.success:
            employees = ListHandler.from_json(response.result_json)
            for employee in employees:
                print(
                    f"ID : {employee.emp_id} Name : {employee.name}, Designation : {employee.designation_code}, Gender : {employee.gender}")
        else:
            er = ExceptionHandler.from_json(response.error_json)
            if er.exceptions is None:
                print(er.message)
            else:
                for exception in er.exceptions.values():
                    print(exception[1])
        print("-" * 50)

    def search_employee_by_id(self):
        """
        Retrieves the desired employee data by taking employee id
        as input at runtime.
        Creates a request class object,
        and sending it via a Wrapper class object to the request class object.
        Then sends it using the NetworkClient class object and receives a response class object.
        This response object is then processed and prints the data sent in the response.
        """
        try:
            emp_id = int(input("Enter the Employee ID : "))
            request = Request(manager="EmployeeManager",
                              action="get_by_id", request_object=Wrapper(emp_id))
            network_client = NetworkClient()
            response = network_client.send(request)
            if response.success:
                employee = Employee.from_json(response.result_json)
                print(
                    f"ID : {employee.emp_id} Name : {employee.name}, Designation : {employee.designation_code}, Gender : {employee.gender}")
            else:
                er = ExceptionHandler.from_json(response.error_json)
                if er.exceptions is None:
                    print(er.message)
                else:
                    for exception in er.exceptions.values():
                        print(exception[1])
        except:
            print(f"ID is of unexpected type, it should be of type {type(0)}")
        print("-" * 50)

    def search_by_name(self):
        """
        Retrieves all the desired employees' data by taking employee's name
        as input at runtime.
        Creates a request class object,
        and sending it via a Wrapper class object to the request class object.
        Then sends it using the NetworkClient class object and receives a response class object.
        This response object is then processed and prints the data sent in the response.
        """
        try:
            name = input("Enter the Name of the Employee : ")
            request = Request(manager="EmployeeManager",
                              action="get_by_name", request_object=Wrapper(name))
            network_client = NetworkClient()
            response = network_client.send(request)
            if response.success:
                employees = ListHandler.from_json(response.result_json)
                for employee in employees:
                    print(
                        f"ID : {employee.emp_id} Name : {employee.name}, Designation : {employee.designation_code}, Gender : {employee.gender}")
            else:
                er = ExceptionHandler.from_json(response.error_json)
                if er.exceptions is None:
                    print(er.message)
                else:
                    for exception in er.exceptions.values():
                        print(exception[1])
        except:
            print("Invalid Entry for Name!!")
        print("-" * 50)

    def search_designation_by_code(self):
        """
        Retrieves the desired designation by taking designation code
        as input at runtime.
        Creates a request class object,
        and sending it via a Wrapper class object to the request class object.
        Then send it using the NetworkClient class object and receives a response class object.
        This response object is then processed and prints the data sent in the response.
        """
        try:
            code = int(input("Enter the Designation Code : "))
            request = Request(manager="DesignationManager",
                              action="getbycode", request_object=Wrapper(code))
            network_client = NetworkClient()
            response = network_client.send(request)
            if response.success:
                designation = Designation.from_json(response.result_json)
                print(
                    f"Code : {designation.code} Designation : {designation.title}")
            else:
                er = ExceptionHandler.from_json(response.error_json)
                if er.exceptions is None:
                    print(er.message)
                else:
                    for exception in er.exceptions.values():
                        print(exception[1])
        except:
            print(
                f"code is of unexpected type, it should be of type {type(0)}")
        print("-" * 50)

    def search_designation_by_title(self):
        """
        Retrieves the desired designation by taking designation title as input at runtime.
        Creates a request class object,
        and sending it via a Wrapper class object to the request class object.
        Then sends it using the NetworkClient class object and receives a response class object.
        This response object is then processed and prints the data sent in the response.
        """
        title = input("Enter the Designation Name : ")
        request = Request(manager="DesignationManager",
                          action="getbytitle", request_object=Wrapper(title))
        network_client = NetworkClient()
        response = network_client.send(request)
        if response.success:
            designation = Designation.from_json(response.result_json)
            print(
                f"Code : {designation.code} Designation : {designation.title}")
        else:
            er = ExceptionHandler.from_json(response.error_json)
            if er.exceptions is None:
                print(er.message)
            else:
                for exception in er.exceptions.values():
                    print(exception[1])
        print("-" * 50)


main_menu = Menu("Main Menu", main_menu_handler)
main_menu.add_option("Designation Master")
main_menu.add_option("Employee Master")
main_menu.add_option("Exit")

designation_menu = Menu("Designation Master", designation_menu_handler)
designation_menu.add_option("Add")
designation_menu.add_option("Edit")
designation_menu.add_option("Delete")
designation_menu.add_option("Search by Code")
designation_menu.add_option("Search by Designation")
designation_menu.add_option("Display List")
designation_menu.add_option("Exit")

employee_menu = Menu("Employee Master", employee_menu_handler)
employee_menu.add_option("Add")
employee_menu.add_option("Edit")
employee_menu.add_option("Delete")
employee_menu.add_option("Search by ID")
employee_menu.add_option("Search by Employee Name")
employee_menu.add_option("Display List")
employee_menu.add_option("Exit")

main_menu.activate()
