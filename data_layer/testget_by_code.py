from hr import Designation, HRDLHandler, DataLayerError
import sys

try:
    code = int(sys.argv[1])
    designation = HRDLHandler.get_designation_by_code(code)
    print(f"Code : {designation.code} Designation : {designation.title}")
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
