import math

from ant_colony_optimization import ACO, Graph
from plot_path import plot

def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)

def main():
    cities = []
    points = []
    with open("./input/city48.txt") as f:
        for line in f.readlines():
            print(line)
            city = line.split(' ')
            cities.append(dict(index=int(city[0]), x=int(city[1]), y=int(city[2])))
            points.append((int(city[1]), int(city[2])))
    distance_d = []
    total_city = len(cities)
    for i in range(total_city):
        row = []
        for j in range(total_city):
            row.append(distance(cities[i], cities[j]))
        distance_d.append(row)
    aco = ACO(100, 1.0, 20.0, 0.5)
    graph = Graph(distance_d, total_city)
    path, cost = aco.solve(graph)
    print('cost: {}, path: {}'.format(cost, path))
    plot(points, path)

if __name__ == '__main__':
    main()
