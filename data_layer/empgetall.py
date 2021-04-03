from hr import Designation, HRDLHandler, DataLayerError

try:
    employees = HRDLHandler.get_employees()
    for employee in employees:
        print(f"ID : {employee.emp_id} Name : {employee.name}, Designation : {employee.designation_code}, Gender : {employee.gender}")
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
