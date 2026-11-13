"""Q3: Complaint word counts, grouping, top-k, and method benchmarks."""
from collections import Counter
import random
import statistics
import string
import time

STOP = {"not", "high", "the", "and", "is", "a", "to"}
SAMPLES = [
    ("seeds not received seeds delayed", "Thanjavur", "paddy"),
    ("fertiliser price high", "Madurai", "cotton"),
    ("seeds price high subsidy not received", "Thanjavur", "paddy"),
]


def tokenize(text):
    table = str.maketrans("", "", string.punctuation)
    return text.lower().translate(table).split()


def frequencies_get(texts, stop=STOP):
    counts = {}
    for text in texts:
        for word in tokenize(text):
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1
    return counts


def frequencies_setdefault(texts, stop=STOP):
    counts = {}
    for text in texts:
        for word in tokenize(text):
            if word not in stop:
                counts.setdefault(word, 0)
                counts[word] += 1
    return counts


def frequencies_list_count(texts, stop=STOP):
    words = [word for text in texts for word in tokenize(text) if word not in stop]
    return {word: words.count(word) for word in set(words)}


def group_by_district(rows):
    grouped = {}
    crop_groups = {}
    for text, district, crop in rows:
        grouped.setdefault(district, []).append(text)
        crop_groups.setdefault(crop, []).append(text)
    return grouped, crop_groups


def top(counts, k):
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:k]


def make_complaints(n, seed=314):
    rng = random.Random(seed)
    templates = [
        ("Seeds not received; seeds delayed!", "Thanjavur", "paddy"),
        ("Fertiliser price high.", "Madurai", "cotton"),
        ("Seeds price high, subsidy not received.", "Thanjavur", "paddy"),
        ("Pest attack on crop; need advice.", "Salem", "maize"),
        ("Market price low for crop", "Erode", "turmeric"),
    ]
    return [templates[rng.randrange(len(templates))] for _ in range(n)]


def benchmark(fn, texts, repeats=3):
    values = []
    for _ in range(repeats):
        start = time.perf_counter(); fn(texts, STOP); values.append(time.perf_counter() - start)
    return statistics.median(values)


def main():
    calls = [row[0] for row in SAMPLES]
    print("sample get counts:", frequencies_get(calls))
    print("sample setdefault counts:", frequencies_setdefault(calls))
    print("top three:", top(frequencies_get(calls), 3))
    by_district, by_crop = group_by_district(SAMPLES)
    print("complaint counts by district:", {k: len(v) for k, v in by_district.items()})
    print("complaints by crop:", {k: len(v) for k, v in by_crop.items()})
    print("empty text and case/punctuation:", frequencies_get(["", "PRICE, price! Seeds?"]))
    print("size,dict_s,list_count_s,counter_s,total_words,distinct_words")
    for n in (1_000, 10_000, 100_000):
        rows = make_complaints(n)
        texts = [row[0] for row in rows]
        dictionary_time = benchmark(frequencies_get, texts)
        list_time = benchmark(frequencies_list_count, texts)
        counter_time = benchmark(lambda t, s: {w: c for w, c in Counter(
            word for text in t for word in tokenize(text) if word not in s).items()}, texts)
        tokens = [word for text in texts for word in tokenize(text) if word not in STOP]
        print(f"{n},{dictionary_time:.6f},{list_time:.6f},{counter_time:.6f},{len(tokens)},{len(set(tokens))}")
        assert frequencies_get(texts) == frequencies_setdefault(texts) == frequencies_list_count(texts)


if __name__ == "__main__":
    main()
