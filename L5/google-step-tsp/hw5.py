import sys
import random
from math import sqrt
from common import print_tour, read_input
import time

# Calculate the distance between two cities.
# 
# |a|: The coordinate of the first city.
# |b|: The coordinate of the second city.
# Return value: The distance between two cities.
def distance(a,b):
    return sqrt(pow(a[0] - b[0], 2.0) + pow(a[1] - b[1], 2.0))

# Calculate the total distance of the route.
#
# |tour|: The list of the cities (the route).
# |dist|: The distance matrix.
# Return value: The sum of the distances between the cities along the route.
def total_distance(tour, dist):
    distance = 0.0
    for i in range(len(tour)-1):
        distance += dist[tour[i]][tour[i+1]]
    distance += dist[tour[-1]][tour[0]]
    return distance

# Get the route by finding the nearest city.
#
# |dist|: The distance matrix.
# |start|: The index of the start city.
# |N|: The number of the cities.
# Return value: The list of cities.
def greedy(dist, start, N):
    unvisited = set(range(0, N))
    unvisited.remove(start)
    tour = [start]
    while unvisited:
        # Current city is the last city in the tour.
        current = tour[-1]
        # Calculate the distance between the current city and all unvisited cities, and choose the nearest city.
        next_city= min(unvisited, key=lambda city: dist[current][city])
        tour.append(next_city)
        unvisited.remove(next_city)
    return tour


# Improve the route by using 2-opt.
#
# |dist|: The distance matrix.
# |tour|: The list of the cities (the route).
# |N|: The number of the cities.
def two_opt(dist, tour, N):
    improvement = True
    while improvement:
        improvement = False
        for i in range(1,N - 2):
            for j in range(i + 2, N):
                # 辺 (i, i+1) と辺 (j, j+1) を交換して改善があるか判定
                root1 = dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[(j+1) % N]]
                root2 = dist[tour[i]][tour[j]] + dist[tour[i+1]][tour[(j+1) % N]]
                if root1 > root2:
                    # 辺の順序を逆にする
                    tour[i + 1:j + 1] = tour[i + 1:j + 1][::-1]
                    improvement = True
    return tour



def solve(cities,cities_list,start):
    N = len(cities_list)
    min_dist = float('inf')

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[cities_list[i]], cities[cities_list[j]])
  
    # print(start,cities_list[start])
    tour = greedy(dist,start,N)
    tour = two_opt(dist,tour,N)
    current_dist = total_distance(tour,dist)
    if current_dist < min_dist:
        min_dist = current_dist
        best_tour = tour
    return best_tour

def divide_cities(cities):
    x_coordinates = [city[0] for city in cities]
    y_coordinates = [city[1] for city in cities]

    x_center = (max(x_coordinates)- min(x_coordinates) )// 2 + min(x_coordinates)
    y_center = (max(y_coordinates)- min(y_coordinates) )// 2 + min(y_coordinates)

    subcities = [[] for _ in range(4)]
    
    for index,city in enumerate(cities):
        x, y = city[0], city[1]
        if x <= x_center and y >= y_center: # Top left
            subcities[0].append(index)
        elif x >= x_center and y >= y_center: # Top right
            subcities[1].append(index)
        elif x >= x_center and y <= y_center: # Bottom right
            subcities[2].append(index)
        elif x <= x_center and y <= y_center: # Bottom left
            subcities[3].append(index)
    return subcities, x_center, y_center

def calc_each_area(cities):
    subcities, x_middle, y_middle = divide_cities(cities)
    tour = []
    for subcity in subcities:
        distances = [distance((x_middle,y_middle),cities[index]) for index in subcity]
        closest_city_index = distances.index(min(distances))
        tour_temp = solve(cities,subcity,closest_city_index)
        tour+=[subcity[index] for index in tour_temp]
    return tour

# for i in `seq 0 6`;do python3 hw5.py input_${i}.csv > output_${i}.csv; done
# python3 hw5.py input_1.csv
# python3 -m http.server
# http://localhost:8000/visualizer/build/default/index.html
if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = calc_each_area(cities)
    print_tour(tour)
