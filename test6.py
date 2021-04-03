from network_client.config import Configuration

c = Configuration()
print(c._obj.host)
print(c._obj.port)
c._validate_values()
print(c._obj.has_exceptions)
print(c._obj.exceptions)
