from random import random
import matplotlib.pyplot as plt
import numpy as np

trials = 10000000
class Test:
    def __init__(self):
        self.values = [random() for x in range(10)]
        self.mean = round(sum(self.values) / 10, 2)
    
fDic = {}

for i in range(trials):
    test = Test()
    m = test.mean
    if m in fDic:
        fDic[m] += 1
    else:
        fDic[m] = 1

a = b = 0
for key, value in fDic.items():
    a += key * value
    b += key * key * value

expectedValue = a / trials
varaince = (b / trials) - (expectedValue * expectedValue)
x = sorted(fDic.keys())
y = [fDic[a] for a in x]

print(expectedValue, varaince)
xPos = np.array(x)
yPos = np.array(y)

plt.plot(xPos, yPos)
plt.show()