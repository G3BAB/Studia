# Author: Jakub Opyrchał (266252)
# Politechnika Wrocławska
# Algorytmy i Struktury Danych
# 14.06.2023 r.
# Code formatted with codebeautify.org

""" To change random city placement generator modify variables in main().
    To change Monte Carlo repetitions modify REPETITIONS in handle_sample().
    To change the sample size limit for brute_force and held_karp modify variables in run_measurement().
    To change axes on a chart modify the set_xlim() or set_ylim() in an appropriate chart generating function."""

import heapq
import time as tm
import random
import matplotlib.pyplot as plot


class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y


def calculate_distance(city1, city2):
    """Calculates distances between cities"""
    return ((city2.x - city1.x) ** 2 + (city2.y - city1.y) ** 2) ** 0.5


def build_distance_matrix(city_set):
    num_cities = len(city_set)
    distance_matrix = [[0] * num_cities for _ in range(num_cities)]

    for i in range(num_cities):
        for j in range(num_cities):
            distance_matrix[i][j] = calculate_distance(city_set[i], city_set[j])

    return distance_matrix


def brute_force(city_set):
    # itercount = 1
    tag = "brute force"
    num_cities = len(city_set)
    result_path = []
    shortest_distance = float("inf")

    def permute(city_set_permute, start=1):
        if start == num_cities - 1:
            distance = 0
            for i in range(num_cities - 1):
                distance += calculate_distance(
                    city_set_permute[i], city_set_permute[i + 1]
                )
            distance += calculate_distance(
                city_set_permute[num_cities - 1], city_set_permute[0]
            )

            nonlocal shortest_distance, result_path
            if distance < shortest_distance:
                shortest_distance = distance
                result_path = city_set_permute[:]

        for i in range(start, num_cities):
            city_set_permute[start], city_set_permute[i] = (
                city_set_permute[i],
                city_set_permute[start],
            )
            permute(city_set_permute, start + 1)
            city_set_permute[start], city_set_permute[i] = (
                city_set_permute[i],
                city_set_permute[start],
            )

    permute(city_set)

    result_path.append(city_set[0])
    return result_path, shortest_distance, tag


def held_karp(city_set):
    tag = "Held Karp"
    num_cities = len(city_set)
    memo = {}

    def solve_tsp(mask, pos):
        if (mask, pos) in memo:
            return memo[(mask, pos)]

        if mask == (1 << num_cities) - 1:
            return calculate_distance(city_set[pos], city_set[0]), [
                city_set[pos],
                city_set[0],
            ]

        min_distance = float("inf")
        min_path = []

        for next_city in range(num_cities):
            if (mask >> next_city) & 1 == 0:
                distance, path = solve_tsp(mask | (1 << next_city), next_city)
                distance += calculate_distance(city_set[pos], city_set[next_city])
                if distance < min_distance:
                    min_distance = distance
                    min_path = [city_set[pos]] + path

        memo[(mask, pos)] = min_distance, min_path
        return min_distance, min_path

    shortest_distance, result_path = solve_tsp(1, 0)

    return result_path, shortest_distance, tag


def nearest_neighbor(city_set):
    tag = "nearest neighbor"
    num_cities = len(city_set)
    visited = [False] * num_cities
    result_path = []
    current_city = city_set[0]
    visited[0] = True
    result_path.append(current_city)
    shortest_distance = 0

    for _ in range(num_cities - 1):
        min_distance = float("inf")
        nearest_city = None

        for i in range(num_cities):
            if not visited[i]:
                distance = calculate_distance(current_city, city_set[i])
                if distance < min_distance:
                    min_distance = distance
                    nearest_city = city_set[i]

        current_city = nearest_city
        visited[city_set.index(nearest_city)] = True
        result_path.append(current_city)
        # print(min_distance)
        # print(current_city.name)
        shortest_distance += min_distance
        # print(total_distance)

    shortest_distance += calculate_distance(result_path[-1], result_path[0])
    result_path.append(result_path[0])

    return result_path, shortest_distance, tag


def minimum_edge(city_set, distance_matrix):
    tag = "minimum edge"

    # print("A")
    # print(distance_matrix)
    num_cities = len(city_set)
    if len(distance_matrix) == 0:
        print("Turbo error")

    queue = []

    visited = [False] * num_cities

    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            heapq.heappush(queue, (distance_matrix[i][j], i, j))

    result_path = [city_set[0]]
    shortest_distance = 0

    next_city = 0
    while len(result_path) < num_cities and queue:
        _, current_city, next_city = heapq.heappop(queue)

        if visited[current_city] or visited[next_city]:
            continue

        result_path.append(city_set[next_city])
        shortest_distance += distance_matrix[current_city][next_city]
        visited[next_city] = True

    result_path.append(city_set[0])
    shortest_distance += distance_matrix[next_city][0]

    return result_path, shortest_distance, tag


def process_results(
    function,
    argument,
    disp_results=False,
    return_time_dist_only=False,
    distance_matrix=None,
):
    """Returns the results as a processable array"""
    # if function is minimum_edge:
    #   print(distance_matrix)
    # if distance_matrix is None:
    #     distance_matrix = []
    time, tag, path, distance = run_measurement(function, argument, distance_matrix)
    result_list = [tag, path, distance, time]

    def announce_results(results):
        """Displays results in the output window"""
        print("{}{}{}".format("Algorytm ", results[0], ":"))
        print("{}{}".format("Droga: ", [city.name for city in results[1]]))
        print("{}{}".format("Odległość: ", results[2]))
        print("{}{}{}".format("Czas wykonania: ", results[3], "ns\n"))

    if disp_results:
        announce_results(result_list)

    result_list.remove(result_list[1])  # removes the path cuz who needs it on a graph

    if return_time_dist_only:
        return time, distance

    else:
        return result_list


def city_generator(num_cities, min_x, max_x, min_y, max_y):
    """Generates random city placement in a plane of given dimensions"""
    cities = []
    for num in range(num_cities):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        cities.append(City(num, x, y))
    return cities


def run_measurement(function, argument, distance_matrix=None):
    """Runs a given funtion while making sure that the more resource-hungry functions are not executed
    for larger sample sizes"""

    BRUTE_FORCE_LIMIT = 11
    HELD_KARP_LIMIT = 17

    if distance_matrix is None:
        distance_matrix = []

    if (len(argument) >= BRUTE_FORCE_LIMIT and function == brute_force) or (
        len(argument) >= HELD_KARP_LIMIT and function == held_karp
    ):

        time = None
        tag = "brute force"
        path = [City(None, None, None)]
        distance = None
        return time, tag, path, distance

    else:
        if function is minimum_edge:
            # print(distance_matrix)
            # print("xd")
            start = tm.perf_counter_ns()
            path, distance, tag = function(argument, distance_matrix)
            stop = tm.perf_counter_ns()
        else:
            start = tm.perf_counter_ns()
            path, distance, tag = function(argument)
            stop = tm.perf_counter_ns()

        time = stop - start
        return time, tag, path, distance


def test():
    city_a = City("A", 0, 0)
    city_b = City("B", 4, 4)
    city_c = City("C", 2, 5)
    city_d = City("D", 2, 8)
    city_e = City("E", 3, 7)

    cities = [city_a, city_b, city_c, city_d, city_e]
    matrix = build_distance_matrix(cities)

    process_results(brute_force, cities, True)
    process_results(held_karp, cities, True)
    process_results(nearest_neighbor, cities, True)
    process_results(minimum_edge, cities, True, False, matrix)


def main():
    # test()
    SAMPLE_SIZES = [
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        15,
        20,
        25,
        50,
        75,
        100,
        150,
        200,
        300,
        400,
        500,
    ]

    # defines the dimensions of the space where cities are located
    X_LOWER = 0
    X_UPPER = 100
    Y_LOWER = 0
    Y_UPPER = 100

    # Agregates all results for all sample sizes and algorithms
    turbo_matrix = []

    def handle_sample(sample_size, x_min, x_max, y_min, y_max):
        """Generates random city placement for a given sample size, then performs
        Monte Carlo calculations"""

        cities = city_generator(sample_size, x_min, x_max, y_min, y_max)
        REPETITIONS = 300

        def monte_carlo(algorithm, city_dataset, dist_matrix=False):
            lowest_time = float("inf")
            highest_time = 0
            matrix = []
            if dist_matrix:
                matrix = build_distance_matrix(city_dataset)
                # print(matrix)

            results = process_results(algorithm, city_dataset, False, False, matrix)
            time = 0
            distance = 0
            matrix = []

            for i in range(REPETITIONS - 1):
                cities_iterate = city_generator(
                    sample_size, X_LOWER, X_UPPER, Y_LOWER, Y_UPPER
                )

                if dist_matrix:
                    # print(matrix)
                    matrix = build_distance_matrix(cities_iterate)

                percentage = (i + 2) / REPETITIONS * 100
                print(
                    "\rN = {} - {}: {}/{} ({:.1f}%)".format(
                        sample_size, algorithm.__name__, i + 2, REPETITIONS, percentage
                    ),
                    end="",
                )
                time, distance = process_results(
                    algorithm, cities_iterate, False, True, matrix
                )
                if time is not None:
                    results[1] += distance
                    results[2] += time

                    if time < lowest_time:
                        lowest_time = time
                    if time > highest_time:
                        highest_time = time

                else:
                    print(
                        "\rN = {} - {}: BYPASSED".format(
                            sample_size, algorithm.__name__
                        ),
                        end="",
                    )
                    break

            # print("")
            if time is not None:
                distance = results[1] / REPETITIONS
                time = results[2] / REPETITIONS

            return results, distance, time, lowest_time, highest_time

        # I'm not proud of this approach
        result_a, mean_distance_a, mean_time_a, lowest_a, highhest_a = monte_carlo(
            brute_force, cities
        )
        result_b, mean_distance_b, mean_time_b, lowest_b, highhest_b = monte_carlo(
            held_karp, cities
        )
        result_c, mean_distance_c, mean_time_c, lowest_c, highhest_c = monte_carlo(
            nearest_neighbor, cities
        )
        result_d, mean_distance_d, mean_time_d, lowest_d, highhest_d = monte_carlo(
            minimum_edge, cities, True
        )

        result_a[1] = mean_distance_a
        result_a[2] = mean_time_a
        result_a.append(lowest_a)
        result_a.append(highhest_a)
        # print(result_a)

        result_b[1] = mean_distance_b
        result_b[2] = mean_time_b
        result_b.append(lowest_b)
        result_b.append(highhest_b)

        result_c[1] = mean_distance_c
        result_c[2] = mean_time_c
        result_c.append(lowest_c)
        result_c.append(highhest_c)

        result_d[1] = mean_distance_d
        result_d[2] = mean_time_d
        result_d.append(lowest_d)
        result_d.append(highhest_d)

        return result_a, result_b, result_c, result_d

    def create_chart(result_matrix, n_samples):
        """Not proud of this one either but it works :)"""
        # print("{}{}".format("BBB: ", len(result_matrix[0])))
        time_data = [[], [], [], []]
        time_highest_data = [[], [], [], []]
        time_lowest_data = [[], [], [], []]
        distance_data = [[], [], [], []]
        tags = []

        # reorganizing arrays because I wrote spaghetti code
        for i in range(len(result_matrix[0])):
            tags.append(result_matrix[0][i][0])
            # print(result_matrix[0][i][0])

            for j in range(len(result_matrix)):
                time_data[i].append(result_matrix[j][i][2])
                # print(result_matrix[j][i][3])
                distance_data[i].append(result_matrix[j][i][1])
                time_lowest_data[i].append(result_matrix[j][i][3])
                # print(time_lowest_data)
                time_highest_data[i].append(result_matrix[j][i][4])

        def chart_time(results, tag):
            nonlocal n_samples
            plot.plot(n_samples, results, label=tag)

        plot.xlabel("Rozmiar próby")
        plot.ylabel("Czas wykonania [ns]")
        plot.title("TSP - Czas wykonania")
        for i in range(len(time_data)):
            chart_time(time_data[i], tags[i])
        ax = plot.gca()
        ax.set_ylim([0, 42000000])
        plot.legend()
        plot.show()

        def chart_brute_force(results, tag):
            nonlocal n_samples
            plot.xlabel("Rozmiar próby")
            plot.ylabel("Czas wykonania [ns]")
            plot.title("Algorytm Naiwny - Czas wykonania")
            plot.plot(n_samples, results[0], label=tag)
            local_ax = plot.gca()
            local_ax.set_xlim([0, 10])

        chart_brute_force(time_data, "Średnia")
        chart_brute_force(time_lowest_data, "Najszybszy czas")
        chart_brute_force(time_highest_data, "Najwolniejszy czas")
        plot.legend()
        plot.show()

        def chart_held_karp(results, tag):
            nonlocal n_samples
            plot.xlabel("Rozmiar próby")
            plot.ylabel("Czas wykonania [ns]")
            plot.title("Algorytm Held Karp - Czas wykonania")
            local_ax = plot.gca()
            local_ax.set_xlim([0, 15])
            # for i in range(len(results)):
            # print(len(n_samples))
            # print(len(results[0]))
            plot.plot(n_samples, results[1], label=tag)

        chart_held_karp(time_data, "Średnia")
        chart_held_karp(time_lowest_data, "Najszybszy czas")
        chart_held_karp(time_highest_data, "Najwolniejszy czas")
        plot.legend()
        plot.show()

        def chart_nearest_neighbor(results, tag):
            nonlocal n_samples
            plot.xlabel("Rozmiar próby")
            plot.ylabel("Czas wykonania [ns]")
            plot.title("Algorytm Nearest Neighbor - Czas wykonania")
            plot.plot(n_samples, results[2], label=tag)

        chart_nearest_neighbor(time_data, "Średnia")
        chart_nearest_neighbor(time_lowest_data, "Najszybszy czas")
        chart_nearest_neighbor(time_highest_data, "Najwolniejszy czas")
        plot.legend()
        plot.show()

        def chart_minimum_edge(results, tag):
            nonlocal n_samples
            plot.xlabel("Rozmiar próby")
            plot.ylabel("Czas wykonania [ns]")
            plot.title("Algorytm Minimum Edge - Czas wykonania")
            plot.plot(n_samples, results[3], label=tag)

        chart_minimum_edge(time_data, "Średnia")
        chart_minimum_edge(time_lowest_data, "Najszybszy czas")
        chart_minimum_edge(time_highest_data, "Najwolniejszy czas")
        plot.legend()
        plot.show()

    for sample in SAMPLE_SIZES:
        # print('{}{}'.format('Rozmiar próby: ', sample))
        result = handle_sample(sample, X_LOWER, X_UPPER, Y_LOWER, Y_UPPER)
        # print(result)
        turbo_matrix.append(result)

    create_chart(turbo_matrix, SAMPLE_SIZES)


main()
