import sys
import random
import numpy as np
from math import sqrt
from common import print_tour, read_input

# Calculate the distance between two cities.
# 
# |a|: The coordinate of the first city.
# |b|: The coordinate of the second city.
# Return value: The distance between two cities.
def dist(a,b):
    return sqrt(pow(a[0] - b[0], 2.0) + pow(a[1] - b[1], 2.0))


# Get the route by finding the nearest city.
#
# |cities|: The list of the cities.
# |start|: The index of the start city.
# |N|: The number of the cities.
# Return value: The list of cities.
def greedy(cities, start, N):
    unvisited = set(range(0, N))
    unvisited.remove(start)
    tour = [start]
    while unvisited:
        # Current city is the last city in the tour.
        current = tour[-1]
        # Calculate the distance between the current city and all unvisited cities, and choose the nearest city.
        next_city= min(unvisited, key=lambda city: dist(cities[current], cities[city]))
        tour.append(next_city)
        unvisited.remove(next_city)
    return tour


# Improve the route by using 2-opt. 
# Pick two random edges and swap them if it reduces the total distance.
#
# |cities|: The list of the cities.
# |tour|: The list of the cities (the route).
# |N|: The number of the cities.
# Return value: The sum of the distances between the cities along the route.
def two_opt(cities,tour,N):
    for _ in range(1000):
        # Pick two indexs randomly. 0 <= a < b < N
        a = random.randint(0,N-3) # N-3: make sure that a left two edeges at least.
        b = random.randint(a+1,N-1)
        # Calculate the distance before and after swapping.
        before = dist(cities[tour[a]], cities[tour[a+1]]) + dist(cities[tour[b]], cities[tour[(b+1)%N]])
        after = dist(cities[tour[a]], cities[tour[b]]) + dist(cities[tour[a+1]], cities[tour[(b+1)%N]])
        # If the distance is reduced, swap the edges.
        if before > after:
            tour[a+1:b+1] = reversed(tour[a+1:b+1])
    return sum(dist(cities[tour[i]],cities[tour[i + 1]]) for i in range(N-1)) + dist(cities[tour[0]],cities[tour[N-1]])


# Calculate the average, minimum, maximum, and variance of the result
#
# |distances|: The list of the distances.
# Return value: The average, minimum, maximum, and variance of the distances.
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
    # Repeat 1000 times(Get random start city for each time.)
    for _ in range(1000):
        # Get random start city.
        start = random.randint(0,N-1)
        # Greedy.
        tour = greedy(cities,start,N)
        # 2-opt. Get the sum of the distances between the cities along the route.
        two_opt_dist = two_opt(cities,tour,N)
        # Update the minimum distance and the route.
        if two_opt_dist < min_dist:
            min_dist = two_opt_dist
            ans = tour
        # distances.append(two_opt_dist)
    # average, minimum, maximum, variance = calculate_stats(distances)
    # print("Average:", average)
    # print("Minimum:", minimum)
    # print("Maximum:", maximum)
    # print("Variance:", variance)
    print_tour(ans)