from hr import Employee, HRDLHandler, DataLayerError

"""
It is used to Update an existing Employee data in the DataBase
"""

try:
    emp_id = int(input("Enter employee ID : "))
    name = input("Enter the name of the Employee : ")
    designation_code = int(input("Enter the designation code : "))
    date = int(input("Enter the date : "))
    month = int(input("Enter the month : "))
    year = int(input("Enter the Year : "))
    salary = float(input("Enter the basic salary : "))
    gender = input("Enter Gender : ")
    indian = int(input("Enter whether the Employee is Indian or not : "))
    pan = input("Enter PAN Number : ")
    aadhar = input("Enter Aadhar Number : ")
    employee = Employee(emp_id, name, designation_code, date,
                        month, year, salary, gender, indian, pan, aadhar)
    HRDLHandler.update_employee(employee)
    print(f"Employee : {name} updated")
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
