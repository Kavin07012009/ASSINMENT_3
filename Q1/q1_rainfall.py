"""Q1: Rainfall lists, slicing, weekly summaries, moving averages and timings."""
import random
import statistics
import time

WINDOW = 7


def weekly_totals(readings):
    return [sum(readings[i:i + 7]) for i in range(0, len(readings) - 6, 7)]


def naive_moving_average(readings, window=WINDOW):
    if len(readings) < window:
        return []
    return [sum(readings[i:i + window]) / window
            for i in range(len(readings) - window + 1)]


def running_moving_average(readings, window=WINDOW):
    if len(readings) < window:
        return []
    total = sum(readings[:window])
    averages = [total / window]
    for i in range(window, len(readings)):
        total += readings[i] - readings[i - window]
        averages.append(total / window)
    return averages


def summarize(readings):
    if not readings:
        return {"weekly": [], "wettest": None, "driest": None,
                "moving_average": [], "dry_days": []}
    weekly = weekly_totals(readings)
    wettest = (max(weekly), weekly.index(max(weekly)) + 1) if weekly else None
    driest = (min(weekly), weekly.index(min(weekly)) + 1) if weekly else None
    return {"weekly": weekly, "wettest": wettest, "driest": driest,
            "moving_average": running_moving_average(readings),
            "dry_days": [i + 1 for i, amount in enumerate(readings) if amount == 0]}


def time_function(fn, readings, repeats=3):
    durations = []
    for _ in range(repeats):
        start = time.perf_counter()
        result = fn(readings)
        durations.append(time.perf_counter() - start)
    return statistics.mean(durations), result


def main():
    sample = [0, 2, 4, 0, 5, 1, 2, 7, 0, 3, 1, 5, 2, 4, 8, 0, 1, 2, 3, 4, 5]
    report = summarize(sample)
    print("sample weekly totals:", report["weekly"])
    print("wettest/driest week (total, week):", report["wettest"], report["driest"])
    print("dry day numbers:", report["dry_days"])
    print("readings[7:14] =", sample[7:14])
    print("readings[-7:] =", sample[-7:])
    print("readings[::7] =", sample[::7])
    print("empty and short moving averages:", naive_moving_average([]), naive_moving_average([1, 2, 3]))
    rng = random.Random(20261113)
    print("days,naive_mean_s,running_mean_s,naive_additions,running_additions,running_subtractions")
    for n in (365, 36_500, 365_000):
        readings = [round(rng.uniform(0, 80), 1) for _ in range(n)]
        naive_time, naive = time_function(naive_moving_average, readings)
        run_time, running = time_function(running_moving_average, readings)
        assert len(naive) == len(running) and all(abs(a - b) < 1e-9 for a, b in zip(naive, running))
        windows = max(0, n - WINDOW + 1)
        naive_adds = WINDOW * windows
        running_adds = 0 if not windows else (WINDOW - 1) + max(0, n - WINDOW)
        running_subtracts = max(0, n - WINDOW)
        print(f"{n},{naive_time:.6f},{run_time:.6f},{naive_adds},{running_adds},{running_subtracts}")


if __name__ == "__main__":
    main()
