# Source Code


```python
import numpy as np
import matplotlib.pyplot as plt

# Globals
WIDTH_SIZE = 8
HEIGHT_SIZE = 6

# Initialize figure and style
fig1 = plt.figure(figsize=(WIDTH_SIZE,HEIGHT_SIZE))
plt.style.use("bmh")

# Create data
X = np.linspace(1, 100, 100)
F1 = lambda x: x
F2 = lambda x: x**2
F3 = lambda x: np.log(x)

# Plot it
plt.plot(X, F1, label='O(N)')
plt.plot(X, F2, label='O(N^2)')
plt.plot(X, F3, label='O(log(N))')

# Format plot and save
plt.title('Scalability of Algorithms')
plt.xlabel('X')
plt.ylabel('Y')
plt.ylim([0, 500])
plt.legend()
plt.grid( axis='both', linestyle='-', linewidth=.5)
plt.savefig('assets/plot.png')
```
