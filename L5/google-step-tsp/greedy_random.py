import sys
import random
import numpy as np
from math import sqrt
from common import print_tour, read_input

def dist(a,b):
    return sqrt(pow(a[0] - b[0], 2.0) + pow(a[1] - b[1], 2.0))

def greedy(cities, start, N):
    # Save index of cities
    unvisited = set(range(0, N))
    unvisited.remove(start)
    tour = [start]
    distance = 0
    while unvisited:
        current = tour[-1]
        next_city= min(unvisited, key=lambda city: dist(cities[current], cities[city]))
        distance += dist(cities[current], cities[next_city])
        tour.append(next_city)
        unvisited.remove(next_city)
    return tour,distance + dist(cities[tour[0]], cities[tour[-1]])

def calculate_stats(distances):
    average = sum(distances) / len(distances)
    minimum = min(distances)
    maximum = max(distances)
    variance = sum((x - average) ** 2 for x in distances) / len(distances)
    return average, minimum, maximum, variance

# for i in `seq 0 6`;do python3 hw5.py input_${i}.csv > output_${i}.csv; done
# python3 hw5.py input_1.csv
# python3 -m http.server
# http://localhost:8000/visualizer/build/default/index.html
if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    N = len(cities)
    min_dist = float('inf')
    distances = []
    for _ in range(1000):
        start = random.randint(0,N-1)
        rtn = greedy(cities,start,N)
        tour = rtn[0]
        distance = rtn[1]
        if distance < min_dist:
            min_dist = distance
            ans = tour
        distances.append(distance)
    # print(ans,min_dist)
    average, minimum, maximum, variance = calculate_stats(distances)
    print("Average:", average)
    print("Minimum:", minimum)
    print("Maximum:", maximum)
    print("Variance:", variance)
    print_tour(ans)