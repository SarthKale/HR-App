from sk_components.components import Wrapper


w = Wrapper(10)
j1 = w.to_json()
print(j1)
a = Wrapper.from_json(j1)
print(a, type(a))

print("-" * 40)

w = Wrapper(True)
j2 = w.to_json()
print(j2)
a = Wrapper.from_json(j2)
print(a, type(a))

print("-" * 40)

w = Wrapper("Good")
j3 = w.to_json()
print(j3)
a = Wrapper.from_json(j3)
print(a, type(a))
