import matplotlib.pyplot as plt

x = [1, 2, 3, 4]   # x-coordinates of the data points
y = [4, 7, 6, 8]   # y-coordinates of the data points

# plotting the data and storing the graph in variable named graph
plt.ion()
graph = plt.plot(x, y)
plt.show()              # showing the resultant graph
