from network_server.server import NetworkServer
from network_common.wrappers import Request, Response, ExceptionHandler, ListHandler
from data_layer.hr import Designation as dld, HRDLHandler, DataLayerError, Employee as dlemp
from all_common.hr import Designation, Employee
from sk_components.components import Wrapper
import json


def requestHandler(request):
    """
    This function process the Request object from the server
    and generates response data by interacting with the data-layer.
    This response data is then wrapped in a Response object
    which is returned to the network server.

    Functionality:
        If the request is the action is in Designation Master,
        the JSON object is converted to Designation object of all_common module
        which is further converted to Designation object of data-layer.
        This object is passed to the appropriate data-layer method and thus retrieve data
        This data is again converted to JSON string and the response object is created.
        This processed object is then returned.
        In another case, if the request is in Employee Master,
        the JSON object is converted to Employee object of all_common module
        which is further converted to the Employee object of data-layer.
        This object is passed to the appropriate data-layer method and thus retrieve data
        This data is again converted to JSON string and the response object is created.
        This processed object is then returned.

        To obtain a convertible Designation/Employee object,
        it often uses Wrapper and List Handler class.
        While if an exception gets raised it uses ExceptionHandler class to be processed
        which can be wrapped in the Response object.

    Arguments:
        request(Request): it is the object that wraps the data required
        to understand the request sent by the client and to process the response.

    Raises:
        DataLayerError:
            if some error occurs at the data layer, it raises DataLayerError.

    Return Value:
        returns the Response object.
    """
    print(request.manager)
    print(request.action)
    print(request.json_string)

    if "designation" in request.manager.lower() and "add" in request.action.lower():
        try:
            designation = Designation.from_json(request.json_string)
            if designation.has_exceptions:
                response = Response(success=False, error=ExceptionHandler(
                    exceptions=designation.exceptions))
                return response
            dl_designation = dld(code=designation.code,
                                 title=designation.title)
            HRDLHandler.add_designation(dl_designation)
            response = Response(success=True)
            return response
        except DataLayerError as dle:
            response = Response(
                success=False, error=ExceptionHandler(**dle.__dict__))
            return response

    if "employee" in request.manager.lower() and "add" in request.action.lower():
        try:
            employee = Employee.from_json(request.json_string)
            if employee.has_exceptions:
                response = Response(success=False, error=ExceptionHandler(
                    exceptions=employee.exceptions))
                return response
            dl_employee = dlemp(**employee.__dict__)
            HRDLHandler.add_employee(dl_employee)
            response = Response(success=True)
            return response
        except DataLayerError as dle:
            response = Response(
                success=False, error=ExceptionHandler(**dle.__dict__))
            return response

    if "employee" in request.manager.lower() and "update" in request.action.lower():
        try:
            employee = Employee.from_json(request.json_string)
            if employee.has_exceptions:
                response = Response(success=False, error=ExceptionHandler(
                    exceptions=employee.exceptions))
                return response
            dl_employee = dlemp(**employee.__dict__)
            HRDLHandler.update_employee(dl_employee)
            response = Response(success=True)
            return response
        except DataLayerError as dle:
            response = Response(
                success=False, error=ExceptionHandler(**dle.__dict__))
            return response

    if "employee" in request.manager.lower() and "remove" in request.action.lower():
        try:
            emp_id = Wrapper.from_json(request.json_string)
            HRDLHandler.delete_employee(emp_id)
            response = Response(success=True)
            return response
        except DataLayerError as dle:
            response = Response(
                success=False, error=ExceptionHandler(**dle.__dict__))
            return response

    if "employee" in request.manager.lower() and "id" in request.action.lower():
        try:
            emp_id = Wrapper.from_json(request.json_string)
            dl_employee = HRDLHandler.get_employee_by_id(emp_id)
            employee = Employee(dl_employee.emp_id, dl_employee.name, dl_employee.designation_code, dl_employee.date, dl_employee.month,
                                dl_employee.year, dl_employee.salary, dl_employee.gender, dl_employee.indian, dl_employee.pan_no, dl_employee.aadhar)
            response = Response(success=True, result_obj=employee)
            return response
        except DataLayerError as dle:
            response = Response(
                success=False, error=ExceptionHandler(**dle.__dict__))
            return response

    if "designation" in request.manager.lower() and "update" in request.action.lower():
        try:
            designation = Designation.from_json(request.json_string)
            if designation.has_exceptions:
                response = Response(success=False, error=ExceptionHandler(
                    exceptions=designation.exceptions))
                return response
            dl_designation = dld(code=designation.code,
                                 title=designation.title)
            HRDLHandler.update_designation(dl_designation)
            response = Response(success=True)
            return response
        except DataLayerError as dle:
            response = Response(
                success=False, error=ExceptionHandler(**dle.__dict__))
            return response

    if "designation" in request.manager.lower() and "remove" in request.action.lower():
        try:
            code = Wrapper.from_json(request.json_string)
            HRDLHandler.delete_designation(code)
            response = Response(success=True)
            return response
        except DataLayerError as dle:
            response = Response(
                success=False, error=ExceptionHandler(**dle.__dict__))
            return response

    if "employee" in request.manager.lower() and "all" in request.action.lower():
        try:
            employees = HRDLHandler.get_employees()
            response = Response(
                success=True, result_obj=ListHandler(employees))
            return response
        except DataLayerError as dle:
            response = Response(
                success=False, error=ExceptionHandler(**dle.__dict__))
            return response

    if "employee" in request.manager.lower() and "name" in request.action.lower():
        try:
            name = json.loads(request.json_string)
            employees = HRDLHandler.get_employee_by_name(name)
            if len(employees) == 0:
                raise DataLayerError(
                    message=f"No Employee with the name : {name}")
            response = Response(
                success=True, result_obj=ListHandler(employees))
            return response
        except DataLayerError as dle:
            response = Response(
                success=False, error=ExceptionHandler(**dle.__dict__))
            return response

    if "designation" in request.manager.lower() and "all" in request.action.lower():
        try:
            designations = HRDLHandler.get_designations()
            response = Response(
                success=True, result_obj=ListHandler(designations))
            return response
        except DataLayerError as dle:
            response = Response(
                success=False, error=ExceptionHandler(**dle.__dict__))
            return response

    if "designation" in request.manager.lower() and "code" in request.action.lower():
        try:
            code = Wrapper.from_json(request.json_string)
            dldesignation = HRDLHandler.get_designation_by_code(code)
            designation = Designation(
                code=dldesignation.code, title=dldesignation.title)
            response = Response(success=True, result_obj=designation)
            return response
        except DataLayerError as dle:
            response = Response(
                success=False, error=ExceptionHandler(**dle.__dict__))
            return response

    if "designation" in request.manager.lower() and "title" in request.action.lower():
        try:
            title = json.loads(request.json_string)
            dldesignation = HRDLHandler.get_designation_by_title(title)
            designation = Designation(
                code=dldesignation.code, title=dldesignation.title)
            response = Response(success=True, result_obj=designation)
            return response
        except DataLayerError as dle:
            response = Response(
                success=False, error=ExceptionHandler(**dle.__dict__))
            return response


network_server = NetworkServer(requestHandler)
network_server.initiate()
