from all_common.hr import Designation
from sk_components.components import Wrapper
from network_common.wrappers import Response
import json


class WhateverError(Exception):
    def __init__(self, message):
        self.message = message

    def to_json(self):
        return json.dumps(self.__dict__)

    def from_json(json_string):
        new_dict = json.loads(json_string)
        return WhateverError(new_dict["message"])


r1 = Response(False, error=WhateverError("Invalid Code : 10"))
jst = r1.to_json()
print(jst)
print("-" * 40)

r2 = Response.from_json(jst)
print("Success :", r2.success)
print("error JSON String :", r2.error_json)
print("result JSON String :", r2.result_json)
print("-" * 40)

ex = WhateverError(r2.error_json)
print(ex.message)
