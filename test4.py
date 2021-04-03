from all_common.hr import Designation
from sk_components.components import Wrapper
from network_common.wrappers import Response

d1 = Designation(-10, "Carpenter")
d1._validate_values()
r1 = Response(True, result_obj=d1)
jst = r1.to_json()
print(jst)
print("-" * 25)
r2 = Response.from_json(jst)
print("Success :", r2.success)
print("Error JSON :", r2.error_json)
print("Result JSON :", r2.result_json)

print("-" * 25)
d2 = Designation.from_json(r2.result_json)
print("Code :", d2.code, "Designation :", d2.title, "Exceptions :", d2.exceptions, "Has Exceptions :", d2.has_exceptions, sep="\n")
