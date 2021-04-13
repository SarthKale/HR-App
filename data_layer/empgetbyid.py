from hr import Designation, HRDLHandler, DataLayerError
import sys

"""
It is used to fetch Employee data by the Employee Id from the DataBase
"""

try:
    emp_id = int(sys.argv[1])
    employee = HRDLHandler.get_employee_by_id(emp_id)
    print(f"ID : {employee.emp_id} Name : {employee.name}, Designation : {employee.designation_code}, Gender : {employee.gender}")
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
