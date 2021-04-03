from hr import Designation, HRDLHandler, DataLayerError

try:
    count = HRDLHandler.get_designation_count()
    print(f"Total records in Designation table : {count}")
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
