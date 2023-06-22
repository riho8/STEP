import sys
from math import sqrt
from common import print_tour, read_input

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
    sum = 0.0
    for i in range(len(tour)-1):
        sum += dist[tour[i]][tour[i+1]]
    sum += dist[tour[-1]][tour[0]]
    return sum


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
    improvementNeeded = True
    while improvementNeeded:
        improvementNeeded = False
        for i in range(1,N - 2):
            for j in range(i + 2, N):
                # If the route is improved by exchanging the edges (i, i+1) and (j, j+1), exchange them.
                root1 = dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[(j+1) % N]]
                root2 = dist[tour[i]][tour[j]] + dist[tour[i+1]][tour[(j+1) % N]]
                if root1 > root2:
                    tour[i + 1:j + 1] = tour[i + 1:j + 1][::-1]
                    # Need to continue to improve the route.
                    improvementNeeded = True
    return tour



# Solve the TSP problem by using greedy and 2-opt.
#
# |cities|: The list of the cities.
# |subcities|: The list of the cities in the particular area.
# |start_index|: The list of the index of the cities in the particular area.
# Return value: The list of the cities in the route.
def solve(cities,subcities,start):
    N = len(subcities)
    min_dist = float('inf')

    # Calculate the distance matrix.
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[subcities[i]], cities[subcities[j]])

    tour = greedy(dist,start,N)
    tour = two_opt(dist,tour,N)

    return tour


# Divide the cities into four areas.
#
# |cities|: The list of the cities.
# Return value: The list of the cities in each area, the middle point of the cities(x,y).
def divide_cities(cities):
    x_coordinates = [city[0] for city in cities]
    y_coordinates = [city[1] for city in cities]

    # Calculate the middle point of the cities.
    x_middle = (max(x_coordinates)- min(x_coordinates) )// 2 + min(x_coordinates)
    y_middle = (max(y_coordinates)- min(y_coordinates) )// 2 + min(y_coordinates)

    # Divide the cities into four areas.
    subcities = [[] for _ in range(4)]
    
    for index,city in enumerate(cities):
        x, y = city[0], city[1]
        if x <= x_middle and y >= y_middle: # Top left
            subcities[0].append(index)
        elif x >= x_middle and y >= y_middle: # Top right
            subcities[1].append(index)
        elif x >= x_middle and y <= y_middle: # Bottom right
            subcities[2].append(index)
        elif x <= x_middle and y <= y_middle: # Bottom left
            subcities[3].append(index)
    return subcities, x_middle, y_middle


# Get the total route by caluclating route for each area.
#
# |cities|: The list of the cities.
# Return value: The list of the cities in the route.
def get_tour_by_area(cities):
    subcities, x_middle, y_middle = divide_cities(cities)
    tour = []
    for subcity in subcities:
        # Get the index of start city(= the nearest city from the middle point of the cities).
        distances = [distance((x_middle,y_middle),cities[index]) for index in subcity]
        closest_city_index = distances.index(min(distances))
        # Get the route for each area.
        tour_temp = solve(cities,subcity,closest_city_index)
        # Convert the index of the cities in each area to the index of the cities in the route.
        tour+=[subcity[index] for index in tour_temp]
    return tour


# for i in `seq 0 6`;do python3 hw5.py input_${i}.csv > output_${i}.csv; done
# python3 hw5.py input_1.csv
# python3 -m http.server
# http://localhost:8000/visualizer/build/default/index.html
if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = get_tour_by_area(cities)
    print_tour(tour)
