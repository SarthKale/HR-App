from hr import Designation, HRDLHandler, DataLayerError

try:
    count = HRDLHandler.get_employee_count()
    print(f"Total records in Employee table : {count}")
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
