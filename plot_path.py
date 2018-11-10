import matplotlib.pyplot as plt

def plot(points, path: list):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    plt.figure(figsize=(100,100))
    for dot in range(1, len(path)):
        i = path[dot - 1]
        j = path[dot]
        plt.plot(x, y, 'co')
        plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='b', length_includes_head=True)
        plt.xlim(0, max(x) * 1.1)
        plt.ylim(0, max(y) * 1.1)
        plt.pause(0.1)
    plt.show()
