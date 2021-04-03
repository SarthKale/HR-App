from hr import Designation, HRDLHandler, DataLayerError
import sys

try:
    name = sys.argv[1]
    employees = HRDLHandler.get_employee_by_name(name)
    for employee in employees:
        print(f"ID : {employee.emp_id} Name : {employee.name}, Designation : {employee.designation_code}, Gender : {employee.gender}")
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
