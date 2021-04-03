from hr import DBConfiguration
# d = DBConfiguration(10, "dfsg", 40, 54, 4657)
d = DBConfiguration("localhost", 50000000, "hrdb", "", None)
print(d.has_exceptions)
print(d.exceptions)
