import sys
import random
import numpy as np
from common import print_tour, read_input

def greedy(cities, start, N):
    # Save index of cities
    unvisited = set(range(0, N))
    unvisited.remove(start)
    tour = [start]
    distance = 0
    while unvisited:
        current = tour[-1]
        current_pos = np.array([cities[current][0], cities[current][1]])
        next_city= min(unvisited, key=lambda city: np.linalg.norm(current_pos - np.array([cities[city][0], cities[city][1]])))
        distance += np.linalg.norm(current_pos - np.array([cities[next_city][0], cities[next_city][1]]))
        tour.append(next_city)
        unvisited.remove(next_city)
    distance += np.linalg.norm(np.array([cities[start][0], cities[start][1]]) - np.array([cities[tour[-1]][0], cities[tour[-1]][1]]))
    return tour, distance

# for i in `seq 0 6`;do python3 hw5.py input_${i}.csv > output_${i}.csv; done
# python3 -m http.server
# http://localhost:8000/visualizer/build/default/index.html
if __name__ == '__main__':
    assert len(sys.argv) > 1
    N = len(read_input(sys.argv[1]))
    min_dist = float('inf')
    for i in range(10):
        start = random.randint(0, N-1)
        ans = greedy(read_input(sys.argv[1]),start,N)
        if ans[1] < min_dist:
            min_dist = ans[1]
            tour = ans[0]
            print(min_dist,tour)
    print_tour(tour)