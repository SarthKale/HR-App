from hr import Designation, HRDLHandler, DataLayerError

try:
    designations = HRDLHandler.get_designations()
    for designation in designations:
        print(f"Code : {designation.code} Designation : {designation.title}")
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
