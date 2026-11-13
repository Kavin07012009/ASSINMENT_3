"""Q2: Tuple keys, aliased grids, copy depth, and memory/time observations."""
import copy
import statistics
import sys
import time


def change_first_row(grid):
    grid[0][0] = 9


def median_seconds(fn, repeats=7):
    samples = []
    for _ in range(repeats):
        start = time.perf_counter(); fn(); samples.append(time.perf_counter() - start)
    return statistics.median(samples)


def main():
    rows, cols = 3, 4
    bad = [[0] * cols] * rows
    bad[0][1] = 7
    good = [[0 for _ in range(cols)] for _ in range(rows)]
    good[0][1] = 7
    print("bad :", bad)
    print("good:", good)
    print("row identity bad/good:", bad[0] is bad[1], good[0] is good[1])
    print("row ids bad:", [id(row) for row in bad])
    print("row ids good:", [id(row) for row in good])

    stops = {(13.0827, 80.2707): "Chennai Central", (13.0418, 80.2341): "T. Nagar"}
    print("tuple-key lookup:", stops[(13.0418, 80.2341)])
    try:
        stops[[13.0418, 80.2341]] = "Invalid key"
    except TypeError as exc:
        print("list key error:", type(exc).__name__, str(exc))

    original = [[1, 2], [3, 4]]
    alias = original
    shallow_copy = copy.copy(original)
    sliced_copy = original[:]
    deep_copy = copy.deepcopy(original)
    print("alias is original:", alias is original)
    print("shallow outer/inner identity:", shallow_copy is original, shallow_copy[0] is original[0])
    print("slice outer/inner identity:", sliced_copy is original, sliced_copy[0] is original[0])
    print("deep outer/inner identity:", deep_copy is original, deep_copy[0] is original[0])
    original[0][0] = 99
    print("after nested mutation shallow/deep:", shallow_copy, deep_copy)
    caller = [1, 2]
    change_first_row([caller])
    print("function changed caller list:", caller)
    tuple_with_list = ([10, 20], "fixed label")
    tuple_with_list[0].append(30)
    print("mutable list inside immutable tuple:", tuple_with_list)

    n = 1_000_000
    values = list(range(n))
    tuple_values = tuple(values)
    list_values = list(values)
    print("container bytes for one million references (elements excluded):",
          sys.getsizeof(tuple_values), sys.getsizeof(list_values))
    index = n - 1
    tuple_create = median_seconds(lambda: tuple(values))
    list_create = median_seconds(lambda: list(values))
    tuple_index = median_seconds(lambda: [tuple_values[index] for _ in range(200_000)])
    list_index = median_seconds(lambda: [list_values[index] for _ in range(200_000)])
    print(f"median creation seconds tuple/list: {tuple_create:.6f}/{list_create:.6f}")
    print(f"median indexing 200k seconds tuple/list: {tuple_index:.6f}/{list_index:.6f}")
    print("zone dictionary sparse alternative: {(row,col):count}; missing keys mean zero")


if __name__ == "__main__":
    main()
