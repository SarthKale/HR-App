from all_common.hr import Designation
from network_common.wrappers import Request

d1 = Designation(10, "Carpenter")
d1._validate_values()
r1 = Request("Designation Master", "add", d1)
jstr = r1.to_json()
print(jstr)
print("*" * 30)

r2 = Request.from_json(jstr)
print("Manager :", r2.manager)
print("Action :", r2.action)
print("JSON String :", r2.json_string)
print("*" * 30)

d2 = Designation.from_json(r2.json_string)
print("Code :", d2.code)
print("Title :", d2.title)
print("Exceptions :", d2.exceptions)
print("Has Exceptions :", d2.has_exceptions)
