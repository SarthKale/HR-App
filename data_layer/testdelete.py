from hr import Designation, HRDLHandler, DataLayerError
import sys

try:
    code = int(sys.argv[1])
    HRDLHandler.delete_designation(code)
    print(f"Designation Code : {code} deleted")
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
