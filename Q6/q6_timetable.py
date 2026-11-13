"""Q6: Nested railway timetable plus station/day index."""
import random
import statistics
import sys
import time


def build_index(timetable):
    index = {}
    for train_no, train in timetable.items():
        for station, arrival, departure in train["stops"]:
            index.setdefault(station, []).append((train_no, arrival, departure, train["days"]))
    return index


def scan_query(timetable, station, day):
    result = []
    for train_no, train in timetable.items():
        if day in train["days"]:
            for stop, arrival, departure in train["stops"]:
                if stop == station:
                    result.append((train_no, arrival, departure))
    return result


def indexed_query(index, station, day):
    return [(train_no, arrival, departure)
            for train_no, arrival, departure, days in index.get(station, []) if day in days]


def make_timetable(n, seed=70):
    rng = random.Random(seed)
    stations = ["Chennai", "Arakkonam", "Katpadi", "Jolarpettai", "Bengaluru", "Salem"]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    result = {}
    for i in range(n):
        chosen = stations[i % len(stations):] + stations[:i % len(stations)]
        stops = []
        base = 300 + i % 600
        for j, name in enumerate(chosen[:3]):
            minute = (base + j * 90 + rng.randrange(15)) % 1440
            arrival = f"{minute // 60:02d}:{minute % 60:02d}"
            departure_min = (minute + 5) % 1440
            departure = f"{departure_min // 60:02d}:{departure_min % 60:02d}"
            stops.append((name, arrival, departure))
        result[f"T{i + 1:05d}"] = {"name": f"Regional Express {i+1}", "stops": stops,
                                   "days": set(days if i % 3 else days[:5])}
    return result


def timed(fn, repeats=7):
    values=[]
    for _ in range(repeats):
        start=time.perf_counter(); fn(); values.append(time.perf_counter()-start)
    return statistics.median(values)


def main():
    table = {
        "12601": {"name": "Coastal Express", "stops": [("Chennai", "06:00", "06:10"), ("Katpadi", "08:00", "08:05"), ("Bengaluru", "11:00", "11:10")], "days": {"Mon", "Wed", "Fri"}},
        "12602": {"name": "Hill Passenger", "stops": [("Chennai", "07:00", "07:05"), ("Katpadi", "09:00", "09:10"), ("Salem", "12:00", "12:05")], "days": {"Tue", "Thu", "Sat"}},
        "12603": {"name": "City Link", "stops": [("Bengaluru", "05:00", "05:10"), ("Katpadi", "07:30", "07:35"), ("Chennai", "10:30", "10:40")], "days": {"Mon", "Tue", "Wed", "Thu", "Fri"}},
        "12604": {"name": "Weekend Special", "stops": [("Chennai", "08:15", "08:20"), ("Arakkonam", "09:15", "09:20"), ("Katpadi", "11:00", "11:05")], "days": {"Sat", "Sun"}},
        "12605": {"name": "Southern Mail", "stops": [("Salem", "04:00", "04:05"), ("Katpadi", "07:00", "07:10"), ("Chennai", "09:45", "09:55")], "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}},
    }
    index = build_index(table)
    for train_no, data in table.items():
        print(f"{train_no} | {data['name']} | days={sorted(data['days'])} | stops={data['stops']}")
    found = [(no, data["name"], next(stop[2] for stop in data["stops"] if stop[0] == "Katpadi"))
             for no, data in table.items()
             if "Mon" in data["days"] and any(s[0] == "Katpadi" for s in data["stops"])]
    print("Monday Katpadi trains sorted by departure:", sorted(found, key=lambda row: row[2]))
    print("unknown station:", indexed_query(index, "Unknown", "Mon"))
    print("train not running that day:", indexed_query(index, "Katpadi", "Sun"))
    print("third station departure expression:", table["12601"]["stops"][2][2])
    print("flat-list alternative: scan every (train, station, arrival, departure, days) record")
    print("trains,build_index_s,scan_query_s,indexed_query_s,shallow_index_bytes,answers_equal")
    for n in (100, 1_000, 10_000):
        data = make_timetable(n)
        build_s = timed(lambda: build_index(data), repeats=3)
        idx = build_index(data)
        scan_s = timed(lambda: scan_query(data, "Katpadi", "Mon"))
        index_s = timed(lambda: indexed_query(idx, "Katpadi", "Mon"))
        expected = scan_query(data, "Katpadi", "Mon")
        equal = sorted(expected) == sorted(indexed_query(idx, "Katpadi", "Mon"))
        extra = sys.getsizeof(idx) + sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in idx.items())
        print(f"{n},{build_s:.6f},{scan_s:.6f},{index_s:.6f},{extra},{equal}")


if __name__ == "__main__":
    main()
