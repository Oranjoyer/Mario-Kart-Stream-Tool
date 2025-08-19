from math import sqrt
from json import dumps

FACTOR = 3
coords = []
for i in range(2*int(21.5/FACTOR)):
    x = FACTOR*i
    y=sqrt(462.25-pow(x-21.5,2))
    coords.append((x+3,int(y)+24))
for i in range(2*int(21.5/FACTOR)):
    x = FACTOR*i
    y=-sqrt(462.25-pow(x-21,2))
    coords.append((int(x+2.5),int(y)+24))
print(dumps(coords))
        