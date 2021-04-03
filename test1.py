from all_common.hr import Designation

d1 = Designation(10, "Carpenter")
d1._validate_values()
jstr = d1.to_json()
print(jstr)
print("*" * 30)
d1 = Designation.from_json(jstr)
print("Code :", d1.code)
print("Title :", d1.title)
print("Exceptions :", d1.exceptions)
print("Has Exceptions :", d1.has_exceptions)
