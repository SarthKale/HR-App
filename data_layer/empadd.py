from hr import Employee, HRDLHandler, DataLayerError

"""
It is used to Add new Employee data into the DataBase
"""

try:
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
    employee = Employee(0, name, designation_code, date,
                        month, year, salary, gender, indian, pan, aadhar)
    HRDLHandler.add_employee(employee)
    print(f"Employee : {name} added")
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
