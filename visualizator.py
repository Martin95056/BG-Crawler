import matplotlib.pyplot as plt
import json

with open('end_servers_histogram.json', 'w') as f:
    data = json.load(f)

x = list(data.keys())
y = list(data.values())

plt.bar(x, y, color='r')

plt.title('Representation of which platforms BG sites uses')
plt.xlabel('Platforms')
plt.ylabel('Quantity')

plt.savefig("histogram.png")
