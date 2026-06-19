#!/usr/bin/env python3
import math
import sys
from common import print_tour, read_input

# calculate the distance between two countries
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

# build an initial route using a greedy algorithm
def greedy(cities):
    n = len(cities)
    curr = 0 # start from the city with index 0
    tour = [curr] # store the order of visited cities
    # list of cities that have not been visited yet (city 0 has already been visited)
    not_visited = []
    for city in range(1, n):
        not_visited.append(city)
    # find the nearest unvisited city from the current city
    while len(not_visited) > 0:
        nearest = None
        nearest_distance = float('inf')
        for city in not_visited:
            d = distance(cities[curr], cities[city])
            if d < nearest_distance:
                nearest_distance = d
                nearest = city
        tour.append(nearest)
        not_visited.remove(nearest)
        curr = nearest
    return tour

# improve the route using 2-opt
def two_opt(cities, tour):
    n = len(tour)
    keep_searching = True
    # repeat edge swaps until the route can no longer be improved
    while keep_searching:
        found_better_route = False
        # try all pairs of edges in the route
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                a = tour[i - 1]
                b = tour[i]
                c = tour[j]
                d = tour[(j + 1) % n]
                current_distance = (
                    distance(cities[a], cities[b])
                    + distance(cities[c], cities[d])
                )
                new_distance = (
                    distance(cities[a], cities[c])
                    + distance(cities[b], cities[d])
                )
                # if reconnecting the edges makes the route shorter,
                # reverse the segment between them and update the route
                if new_distance < current_distance:
                    tour[i:j + 1] = reversed(tour[i:j + 1])
                    found_better_route = True
        if found_better_route == False:
            keep_searching = False
    return tour

# generate the final route
def solve(cities):
    tour = greedy(cities)
    tour = two_opt(cities, tour)
    return tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
