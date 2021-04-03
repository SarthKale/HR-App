from hr import Designation, HRDLHandler, DataLayerError
import sys

try:
    code = int(sys.argv[1])
    title = sys.argv[2]
    designation = Designation(code, title)
    HRDLHandler.update_designation(designation)
    print(f"Designation : {title} updated")
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
