from hr import Employee, HRDLHandler, DataLayerError

"""
It is used to Delete a single Employee data from the DataBase
"""

try:
    emp_id = int(input("Enter employee ID : "))
    HRDLHandler.delete_employee(emp_id)
    print(f"Employee : {emp_id} deleted")
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
