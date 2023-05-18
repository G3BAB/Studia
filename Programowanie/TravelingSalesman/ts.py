import random
import math


def make_cities(num_cities, min_x, max_x, min_y, max_y):
    cities = []
    for num in range(num_cities):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        cities.append((x, y))
    return cities


def make_distance_matrix(cities_set, num_cities):
    def calculate_distance(city1, city2):
        x1, y1 = city1
        x2, y2 = city2
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance

    distance_matrix = [[0.0] * num_cities for i in range(num_cities)]

    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            distance = calculate_distance(cities_set[i], cities_set[j])
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance

    return distance_matrix


def brute_force(cities_set, distance_matrix):
    num_cities = len(cities_set)
    best_path = None
    best_distance = float('inf')
    iter_counter = 0

    def permute(cities, start_index):
        nonlocal best_path
        nonlocal best_distance
        nonlocal iter_counter

        if start_index == num_cities - 1:
            current_distance = 0
            for i in range(num_cities - 1):
                current_distance += distance_matrix[cities[i]][cities[i + 1]]

            if current_distance < best_distance:
                best_distance = current_distance
                best_path = cities[:]

            iter_counter += 1

        for i in range(start_index, num_cities):
            cities[start_index], cities[i] = cities[i], cities[start_index]
            permute(cities, start_index + 1)
            cities[start_index], cities[i] = cities[i], cities[start_index]

    initial_permutation = list(range(num_cities))
    permute(initial_permutation, 0)

    print(iter_counter)
    return best_path, best_distance


def held_karp(cities_set):
    return 0


def nearest_neighbor(cities_set):
    return 0


def least_edge(cities_set):
    return 0


def monte_carlo():
    return 0


def traveling_salesman(num_cities, x_min, x_max, y_min, y_max):
    debug = 0

    cities = make_cities(num_cities, x_min, x_max, y_min, y_max)
    distance_matrix = make_distance_matrix(cities, num_cities)

    if debug == 1:
        print(cities)
        for row in distance_matrix:
            print(row)

    brute_force(cities, distance_matrix)


# Defines the boundaries of the (X, Y) plane
x_lower = 0
x_upper = 100

y_lower = 0
y_upper = 100

n_cities = 10

traveling_salesman(n_cities, x_lower, x_upper, y_lower, y_upper)