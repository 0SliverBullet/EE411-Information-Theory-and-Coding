import matplotlib.pyplot as plt
import math

import numpy as np

x = range(1, 26)
y = []

for k in x:
    result = (math.factorial(25) / (math.factorial(k) * math.factorial(25 - k))) * (0.6 ** k) * (0.4 ** (25 - k))
    y.append(result)

sum=0
for i in range(25):
    if 24-i+1 in range(13,20):
     sum+=y[24-i]
     print(24-i+1,sum,y[24-i])

#print(y)

plt.plot(x, y)
plt.xlabel('k')
plt.ylabel('y')
plt.title('Graph of y = (25! / (k! * (25-k)!)) * 0.6^k * 0.4^(25-k)')
plt.show()