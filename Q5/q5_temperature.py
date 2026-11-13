"""Q5: Clean and convert sensor data using loops, comprehensions and map/filter."""
import random
import statistics
import sys
import time


def loop_version(readings):
    celsius, fahrenheit = [], []
    alarms = []
    for minute, value in enumerate(readings):
        if -50 <= value <= 50:
            celsius.append(value)
            fahrenheit.append(value * 9 / 5 + 32)
        if not 2 <= value <= 8:
            alarms.append(minute)
    return celsius, fahrenheit, alarms


def comprehension_version(readings):
    celsius = [value for value in readings if -50 <= value <= 50]
    fahrenheit = [value * 9 / 5 + 32 for value in readings if -50 <= value <= 50]
    alarms = [minute for minute, value in enumerate(readings) if not 2 <= value <= 8]
    return celsius, fahrenheit, alarms


def map_filter_version(readings):
    valid = list(filter(lambda value: -50 <= value <= 50, readings))
    celsius = list(map(lambda value: value, valid))
    fahrenheit = list(map(lambda value: value * 9 / 5 + 32, valid))
    alarms = list(map(lambda pair: pair[0], filter(
        lambda pair: not 2 <= pair[1] <= 8, enumerate(readings))))
    return celsius, fahrenheit, alarms


def median_time(fn, readings, repeats=3):
    values=[]
    for _ in range(repeats):
        start=time.perf_counter(); result=fn(readings); values.append(time.perf_counter()-start)
    return statistics.median(values), result


def main():
    sample = [-51, -2, 3, 9, 51, 7, 0]
    versions = [loop_version(sample), comprehension_version(sample), map_filter_version(sample)]
    print("sample results:", versions[0])
    print("three versions equal:", versions[0] == versions[1] == versions[2])
    print("all valid/all invalid:", comprehension_version([3, 4]), comprehension_version([-70, 80]))
    print("n,loop_s,comprehension_s,map_filter_s,identical")
    rng = random.Random(512)
    for n in (10_000, 100_000, 1_000_000):
        readings = [rng.uniform(-60, 60) for _ in range(n)]
        t1, a = median_time(loop_version, readings)
        t2, b = median_time(comprehension_version, readings)
        t3, c = median_time(map_filter_version, readings)
        print(f"{n},{t1:.6f},{t2:.6f},{t3:.6f},{a == b == c}")
    valid = [2.0 + (i % 7) for i in range(10_000)]
    generator = (value * 9 / 5 + 32 for value in valid if -50 <= value <= 50)
    list_result = [value * 9 / 5 + 32 for value in valid if -50 <= value <= 50]
    print("container bytes list/generator:", sys.getsizeof(list_result), sys.getsizeof(generator))
    print("generator-expression streaming sum:", sum(value for value in valid if -50 <= value <= 50))


if __name__ == "__main__":
    main()
