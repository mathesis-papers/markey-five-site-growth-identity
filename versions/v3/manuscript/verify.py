import argparse
from collections import Counter
import json
from pathlib import Path


DIRECTIONS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
MOVES = ((1, 1), (-1, 2), (2, -1), (-1, -1), (1, -2), (-2, 1))


def advance(state):
    neighbors = Counter((horizontal + delta_x, vertical + delta_y)
                        for horizontal, vertical in state
                        for delta_x, delta_y in DIRECTIONS)
    return state | {point for point, count in neighbors.items() if count >= 2}


def shape(seed_size, iteration):
    length = seed_size - 1 + 2 * iteration
    points = set()
    for first in range(length + 1):
        for second in range(first % 3, length + 1, 3):
            if iteration < first + second < 2 * length - iteration:
                points.add(((2 * first + second) // 3 - iteration,
                            (second - first) // 3))
    return points


def formula(seed_size, iteration):
    if iteration == 0:
        return seed_size
    if seed_size == 2:
        correction = (0, 4, 2)[iteration % 3]
        return (3 * iteration ** 2 + 5 * iteration + correction) // 3
    if seed_size == 3:
        return iteration ** 2 + 3 * iteration + (1 if iteration % 3 == 0 else 3)
    if seed_size == 4:
        return (3 * iteration ** 2 + 13 * iteration + 12 + 2 * (iteration % 3)) // 3
    if iteration == 1:
        return 13
    return (3 * iteration ** 2 + 17 * iteration + 25 - 2 * ((iteration - 1) % 3)) // 3


def inside(first, second, corner, length):
    return (0 <= first <= length and 0 <= second <= length
            and corner <= first + second <= 2 * length - corner)


def check_boundary():
    configurations = 0
    points = 0
    for corner in range(3, 11):
        for length in range(corner + 2, corner + 11):
            configurations += 1
            for first in range(-3, length + 4):
                for second in range(-3, length + 4):
                    old = inside(first, second, corner, length)
                    count = sum(inside(first + delta_x, second + delta_y, corner, length)
                                for delta_x, delta_y in MOVES)
                    expanded = inside(first + 1, second + 1, corner + 1, length + 2)
                    assert expanded == (old or count >= 2), (corner, length, first, second)
                    points += 1
    return {'corner_range': [3, 10], 'length_minus_corner_range': [2, 10],
            'configurations': configurations, 'points': points,
            'coordinate_range': '[-3,L+3] in each coordinate'}


def run(maximum):
    counts = {}
    edges = {}
    regions = {}
    boundary_incidence_comparisons = 0
    shape_comparisons = 0
    for seed_size in range(2, 6):
        state = {(horizontal, 0) for horizontal in range(seed_size)}
        previous = set()
        values = []
        for iteration in range(maximum + 1):
            values.append(len(state))
            assert len(state) == formula(seed_size, iteration), (seed_size, iteration)
            if iteration >= 2:
                assert state == shape(seed_size, iteration), (seed_size, iteration)
                shape_comparisons += 1
            if seed_size == 2 and iteration >= 1:
                incidence = sum((horizontal + delta_x, vertical + delta_y) in state
                                for horizontal, vertical in previous
                                for delta_x, delta_y in DIRECTIONS)
                expected_edge = (6 if iteration == 1 else
                                 6 * iteration ** 2 - 4 * iteration
                                 + (2 if iteration % 3 == 2 else -2))
                expected_region = (3 if iteration == 1 else
                                   (15 * iteration ** 2 - 17 * iteration
                                    + (-3, -7, 7)[iteration % 3]) // 3)
                assert incidence == expected_edge, (iteration, incidence, expected_edge)
                assert incidence - len(state) + 1 == expected_region
                edges[iteration] = incidence
                regions[iteration] = expected_region
                if iteration >= 3:
                    coordinate_face = ((2 * iteration - 1) // 3
                                       - (iteration - 1) // 3)
                    sum_face = (iteration - (2 * iteration) % 3) // 3 + 1
                    assert incidence == 6 * len(previous) - 4 * coordinate_face - 2 * sum_face
                    boundary_incidence_comparisons += 1
            if iteration < maximum:
                previous = state
                state = advance(state)
        counts[seed_size] = values
    for iteration in range(2, maximum + 1):
        assert counts[5][iteration] == counts[2][iteration] + 4 * iteration + 7
    for iteration in range(2, maximum - 1):
        assert (counts[5][iteration + 2] - 2 * counts[5][iteration + 1]
                + counts[5][iteration]) == 2 * (iteration % 3)
    for iteration in range(1, maximum - 1):
        assert (counts[3][iteration + 2] - 2 * counts[3][iteration + 1]
                + counts[3][iteration]) == (6 if iteration % 3 == 2 else 0)
    for iteration in range(maximum - 1):
        assert (counts[4][iteration + 2] - 2 * counts[4][iteration + 1]
                + counts[4][iteration]) == (2, 0, 4)[iteration % 3]
    numerators = {3: [3, 1, 2, -3, 5, -2], 4: [4, 2, 2, -4, 2],
                  5: [5, 3, 2, -5, 1, -2, 2]}
    denominator = [1, -2, 1, -1, 2, -1]
    for seed_size, numerator in numerators.items():
        for iteration in range(maximum + 1):
            coefficient = sum(multiplier * counts[seed_size][iteration - offset]
                              for offset, multiplier in enumerate(denominator)
                              if iteration >= offset)
            expected = numerator[iteration] if iteration < len(numerator) else 0
            assert coefficient == expected, (seed_size, iteration, coefficient)
    added_circles = [counts[2][0]] + [counts[2][iteration] - counts[2][iteration - 1]
                                      for iteration in range(1, maximum + 1)]
    circle_denominator = [1, -1, 0, -1, 1]
    circle_numerator = [2, 0, 2, 0, 4, -2]
    for iteration in range(maximum + 1):
        coefficient = sum(multiplier * added_circles[iteration - offset]
                          for offset, multiplier in enumerate(circle_denominator)
                          if iteration >= offset)
        assert coefficient == (circle_numerator[iteration] if iteration < 6 else 0)
    petal_numerator = [0, 1, 5, 6, 11, -5]
    petals = []
    for iteration in range(maximum + 4):
        coefficient = petal_numerator[iteration] if iteration < 6 else 0
        coefficient -= sum(multiplier * petals[iteration - offset]
                           for offset, multiplier in enumerate(denominator)
                           if offset and iteration >= offset)
        petals.append(coefficient)
    for iteration in range(2, maximum + 1):
        assert petals[iteration + 3] == 3 * counts[5][iteration] - 2
    for iteration in range(1, maximum + 1):
        assert petals[iteration] == 3 * counts[2][iteration] - 6 * iteration - 5
    return {'status': 'pass', 'arithmetic': 'exact integers',
            'iteration_range': [0, maximum], 'seed_sizes': [2, 3, 4, 5],
            'shape_comparisons': shape_comparisons,
            'count_comparisons': 4 * (maximum + 1),
            'difference_comparisons': maximum - 1,
            'second_difference_comparisons': maximum - 3,
            'three_site_second_difference_comparisons': maximum - 2,
            'four_site_second_difference_comparisons': maximum - 1,
            'power_series_coefficients': 3 * (maximum + 1),
            'edge_incidence_comparisons': maximum,
            'region_formula_comparisons': maximum,
            'boundary_incidence_comparisons': boundary_incidence_comparisons,
            'added_circle_coefficients': maximum + 1,
            'petal_coefficient_relations': maximum - 1,
            'petal_vertex_coefficient_relations': maximum,
            'petal_scope': 'Coefficients of the stated rational series; geometric petal counts are separate.',
            'initial_edges': [edges[iteration] for iteration in range(1, min(maximum, 10) + 1)],
            'initial_regions': [regions[iteration] for iteration in range(1, min(maximum, 10) + 1)],
            'boundary_checks': check_boundary(),
            'initial_counts': {str(size): values[:11] for size, values in counts.items()},
            'scope': 'Finite comparisons of simultaneous lattice evolution, exact shapes, '
                     'closed formulas, circle incidences, region formulas, added-circle and petal '
                     'power-series coefficients, and the hexagon boundary law.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--maximum', type=int, default=60)
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    if not 7 <= arguments.maximum <= 200:
        parser.error('--maximum must lie between 7 and 200')
    result = json.dumps(run(arguments.maximum), indent=2, sort_keys=True) + '\n'
    if arguments.output:
        arguments.output.write_text(result)
    print(result, end='')


if __name__ == '__main__':
    main()
