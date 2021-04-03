from network_common.wrappers import ListHandler
from data_layer.hr import Designation

d1 = Designation(1, "Sarthak")
d2 = Designation(2, "Shantanu")
d3 = Designation(3, "Sir")

lst = ListHandler([d1, d2, d3])
l1 = []
json_str = lst.to_json()
designations = ListHandler.from_json(json_str)
for designation in designations:
    l1.append(Designation(designation.code, designation.title))
for item in l1:
    print("Code:", item.code, "Title:", item.title)