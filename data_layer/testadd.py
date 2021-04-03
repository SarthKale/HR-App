from hr import Designation, HRDLHandler, DataLayerError
import sys

try:
    title = sys.argv[1]
    designation = Designation(0, title)
    HRDLHandler.add_designation(designation)
    print(f"Designation : {title} added")
except DataLayerError as dle:
    print(dle.message)
    print(dle.exceptions)
