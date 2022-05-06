import numpy as np


with open("test.txt") as f:
    data = f.read()

li_a = [a for a in data.split("\n")]
print(li_a)

for l in li_a:
    attributes = l.split(",")
    print(attributes) if not len(attributes) < 5 else print("xd")
    print("===========")
