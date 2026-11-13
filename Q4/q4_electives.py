"""Q4: Elective set operations, membership and intersection benchmarks."""
import statistics
import time


def nested_common(left, right):
    return {x for x in left for y in right if x == y}


def median_time(fn, repeats=5):
    values = []
    for _ in range(repeats):
        start = time.perf_counter(); fn(); values.append(time.perf_counter() - start)
    return statistics.median(values)


def main():
    ai = {"192311001", "192311004", "192311007", "192311009", "192311009"}
    iot = {"192311002", "192311004", "192311009", "192311010"}
    all_students = {f"1923110{i:02d}" for i in range(1, 11)}
    both = ai & iot
    exactly_one = ai ^ iot
    neither = all_students - (ai | iot)
    print("clash      :", sorted(both))
    print("exactly one:", sorted(exactly_one))
    print("neither    :", sorted(neither))
    # Repeat using named set methods and confirm identical results.
    both_m = ai.intersection(iot)
    one_m = ai.symmetric_difference(iot)
    neither_m = all_students.difference(ai.union(iot))
    print("operators equal set methods:", (both, exactly_one, neither) == (both_m, one_m, neither_m))
    empty = set()
    print("empty electives:", empty & ai, empty ^ ai, all_students - (empty | ai))
    print("identical electives:", ai & ai, ai ^ ai, ai - ai)
    print("small case hand check (A={a,b}, B={b,c}):", {"a", "b"} & {"b", "c"}, {"a", "b"} ^ {"b", "c"})
    try:
        { [1, 2] }
    except TypeError as exc:
        print("list-in-set error:", type(exc).__name__)
    print("tuple-in-set works:", {(1, 2), (3, 4)})
    print("n,list_membership_s,set_membership_s,nested_s,ampersand_s")
    for n in (10_000, 100_000, 1_000_000):
        values = [f"R{i:08d}" for i in range(n)]
        value_set = set(values)
        target = values[-1]
        reps = 100 if n == 1_000_000 else 1_000
        list_time = median_time(lambda: [target in values for _ in range(reps)])
        set_time = median_time(lambda: [target in value_set for _ in range(reps)])
        # Nested loops are measured separately on a tractable 1,500 x 1,500 fixture.
        if n == 10_000:
            left = values[:1500]
            right = values[750:2250]
            nested_time = median_time(lambda: nested_common(left, right), repeats=3)
            set_time_small = median_time(lambda: set(left) & set(right), repeats=3)
            print(f"nested fixture 1500x1500: {nested_time:.6f}s; set &: {set_time_small:.6f}s")
        print(f"{n},{list_time:.6f},{set_time:.6f},NA,NA")


if __name__ == "__main__":
    main()
