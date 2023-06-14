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
    return tour

def two_opt(cities,tour,N):
    for _ in range(100):
        a = random.randint(0,N-3)
        b = random.randint(a+1,N-1)
        before = dist(cities[tour[a]], cities[tour[a+1]]) + dist(cities[tour[b]], cities[tour[(b+1)%N]])
        after = dist(cities[tour[a]], cities[tour[b]]) + dist(cities[tour[a+1]], cities[tour[(b+1)%N]])
        if before > after:
            tour[a+1:b+1] = reversed(tour[a+1:b+1])
    return sum(dist(cities[tour[i]],cities[tour[i + 1]]) for i in range(N-1)) + dist(cities[tour[0]],cities[tour[N-1]])

# for i in `seq 0 6`;do python3 hw5.py input_${i}.csv > output_${i}.csv; done
# python3 hw5.py input_1.csv
# python3 -m http.server
# http://localhost:8000/visualizer/build/default/index.html
if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    N = len(cities)
    min_dist = float('inf')
    for i in range(N):
        start = i
        tour = greedy(cities,start,N)
        # print(start,tour)
        two_opt_dist = two_opt(cities,tour,N)
        if two_opt_dist < min_dist:
            min_dist = two_opt_dist
            ans = tour
    # print(ans,min_dist)
    print_tour(ans)