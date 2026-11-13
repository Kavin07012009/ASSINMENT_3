# Python Programming Assignment 3 CO3

**Student:** [Enter full name]  
**Register number:** [Enter register number]  
**GitHub repository:** [Paste the repository URL here]  
**Python used for execution evidence:** Python 3.14.7  
**Libraries:** Python standard library only

The seven task programs are in the matching `Q1`–`Q7` folders. Timings and memory results below were collected by running those programs on Python 3.14.7. Values are machine-specific; raw outputs are saved beside each program and under `evidence/`.

## Q1 Lists and slicing Daily rainfall records

### Design and hand checks

Readings belong in a list because the daily sequence is ordered, supports indexing/slicing and is built incrementally. `readings[7:14]` returns indices 7 through 13 (the eighth through fourteenth values); `readings[-7:]` returns the last seven entries; `readings[::7]` selects every seventh entry from index zero. The program reports 7-day weekly totals for complete weeks and leaves any incomplete final block out of the weekly comparison. It reports the 1-based week positions of the wettest and driest totals and the 1-based day positions of zero readings.

Moving-average pseudocode: if fewer than seven readings, return an empty list; sum the first seven; save its mean; for each new day, subtract the outgoing value and add the incoming value, then save the new mean. Empty and three-value inputs both produce `[]`.

### Measurements and operation counts

| Days n | Naive mean (s) | Running mean (s) | Naive additions 7(n−6) | Running additions | Running subtractions |
|---:|---:|---:|---:|---:|---:|
| 365 | 0.000038 | 0.000016 | 2,513 | 364 | 358 |
| 36,500 | 0.003309 | 0.001136 | 255,458 | 36,499 | 36,493 |
| 365,000 | 0.033932 | 0.011886 | 2,554,958 | 364,999 | 364,993 |

The naive method recalculates seven values for every window, so it performs 7(n−6) additions. The running sum initializes with six additions and then adds one incoming reading for each new window, for n−1 additions total, plus n−7 subtractions. It was faster at each tested size. Both produce identical averages. The output list takes O(n) space; the running total itself takes O(1) extra space.

List `append` and end `pop` are amortized O(1); `insert` or removal near the front/middle shifts later entries and costs O(n); comparison sort costs O(n log n). A late reading inserted into its dated position therefore costs O(n) to shift values. A list remains practical for one year of readings; for frequent late inserts, a date-keyed mapping or database table may be more suitable.

A `deque(maxlen=7)` can maintain a constant-size window while streaming readings, giving O(n) processing and O(7) window storage. With list slicing, summing each slice costs O(7n), which is O(n) for fixed window 7 but repeats additions. A date dictionary offers average O(1) keyed access but needs a date-order rule for sequential windows and O(n) storage.

## Q2 Tuples Mutability and copying

A stop coordinate is represented by a tuple and used as the key in `stops`; `(13.0418, 80.2341)` retrieves “T. Nagar”. A list key raises `TypeError` because lists are mutable and unhashable. Tuples can be dictionary keys when all their elements are hashable.

The incorrect grid `[[0] * cols] * rows` repeats references to the same inner list. In the observed output, `bad[0] is bad[1]` is `True`, and changing one cell changes every row. The corrected comprehension creates a fresh row each time, so identity is `False` and only one row changes.

```text
Aliased:       bad ──► row A ◄── row A ◄── row A
Corrected:     good ─► row A   row B   row C
```

An alias is the same outer object. `copy.copy` and slicing create new outer lists but retain references to nested rows; changes to nested mutable values show through. `copy.deepcopy` recursively copies nested objects. Shallow copying is enough when nested items are immutable or intentionally shared. A function receiving a list can mutate the same list object the caller passed, which is demonstrated by changing caller's first element.

The tuple and list containers holding one million references occupied **8,000,048 bytes** and **8,000,056 bytes** respectively with this interpreter. `getsizeof` counts each container but not the referenced integer objects; the tuple/list refer to the same integer values in this comparison. Median creation times were **0.001848 s** for a tuple and **0.001166 s** for a list; 200,000 index reads took **0.001745 s** and **0.001772 s**. Both indexing operations are O(1); these close timings are not a meaningful general performance distinction. A tuple protects a fixed collection of references from being reassigned, but it does not make a mutable object inside it immutable: the list inside `([10, 20], "fixed")` can still be appended to.

For sparse passenger zones, a dictionary keyed by `(row, column)` stores only nonempty counts. Lookup is O(1) average, like a dense grid, while storage is O(number of nonempty zones) rather than O(rows × columns); missing keys mean zero. A dense list remains simpler when most zones are used.

## Q3 Dictionaries Farmer helpline complaint analysis

The program lowercases text, removes punctuation, drops the stop-word set, and counts words with both `dict.get()` and `dict.setdefault()`. It groups text by district and crop with lists and ranks by descending count followed by alphabetical word order. For the sample, the top results are `seeds: 3`, `price: 2`, `received: 2`. `price` comes before `received` because their counts tie and alphabetical order breaks the tie. Empty text gives no counts; uppercase and punctuation normalize correctly.

| Complaints | Dictionary (s) | `list.count` (s) | `Counter` (s) | Tokens | Distinct non-stop words |
|---:|---:|---:|---:|---:|---:|
| 1,000 | 0.000734 | 0.001057 | 0.000717 | 4,177 | 15 |
| 10,000 | 0.007226 | 0.010389 | 0.007409 | 41,951 | 15 |
| 100,000 | 0.073520 | 0.104107 | 0.075465 | 419,937 | 15 |

A dictionary hashes a key to locate its bucket; lookup and update are O(1) average, though collisions and adversarial cases can increase work. For n tokens and d distinct words, dictionary counting and `Counter` take O(n) average time and O(d) count storage. Calling `list.count()` once for every distinct token scans all n tokens each time, O(n·d), and uses O(n) to retain the token list. At 100,000 complaints the dictionary loop was faster than `list.count`; `Counter` was marginally fastest in this run. I would deploy `Counter` or the explicit dictionary loop for a daily 100,000-record load, with the dictionary loop easier to customize during token processing.

Python 3.7 and later preserve dictionary insertion order. `keys()`, `values()`, and `items()` return dynamic views over keys, values, or key-value pairs; they reflect changes to the dictionary rather than making copied lists. A list of grouped complaint texts costs O(n) total storage.

## Q4 Sets Elective registration clash detection

Sets remove duplicate registrations automatically. `&` returns students in both electives, `^` those in exactly one, `|` all registered students, and `all_students - (ai | iot)` students in neither. The sample results are:

```text
AI only:      192311001, 192311007
Both:         192311004, 192311009
IoT only:     192311002, 192311010
Neither:      192311003, 192311005, 192311006, 192311008
```

The Venn regions can be read as follows (each registration appears in only one region):

```text
        AI elective                 IoT elective
      _____________               _____________
     /             \             /             \
    / AI only       \___________/ IoT only      \
   | 001, 007       | 004, 009   | 002, 010      |
    \              /‾‾‾‾‾‾‾‾‾‾‾\              /
     \____________/             \____________/

Outside both circles: 003, 005, 006, 008
```

The `&`, `^`, `-`, and `|` expressions matched the named set methods. Empty and identical sets were also checked, along with a hand-calculated `{a,b}` / `{b,c}` example. Sets require hashable elements, so a list cannot be a member but a tuple can. Convert a list to a set when duplicate removal or repeated membership checks matter; the conversion discards ordering and multiplicity.

| n registrations | `x in list` (s) | `x in set` (s) |
|---:|---:|---:|
| 10,000 | 0.046111 | 0.000012 |
| 100,000 | 0.463618 | 0.000010 |
| 1,000,000 | 0.461533 | 0.000001 |

Each timing repeats a last-element lookup (1000 repetitions except 100 at one million); interpreter resolution makes the smallest set timings noisy. Membership in a list scans O(n), while set membership is O(1) average. On 1,500 × 1,500 inputs, the nested-loop common-student search took **0.011440 s** and set intersection took **0.000071 s**. Nested loops are O(nm), sorting both lists then walking them is O(n log n + m log m), and set operations are O(n+m) average. Set operations allocate result sets, generally O(n+m) output storage.

## Q5 List comprehension Cleaning sensor readings

A reading is valid when `-50 <= c <= 50`. The program returns valid Celsius values, their Fahrenheit conversions, and minute indices with values outside 2–8 °C. A loop with `append`, two list-comprehension filters, and `map`/`filter`/lambda versions produce identical outputs for the normal, all-valid, and all-invalid examples. The comprehension form is `[expression for item in iterable if condition]`. A comprehension is less clear when it contains several nested conditions, side effects, or multiple actions; use a loop then. Dictionary and set comprehension examples are `{i: c * 9 / 5 + 32 for i, c in enumerate(readings) if -50 <= c <= 50}` and `{i for i, c in enumerate(readings) if not 2 <= c <= 8}`. A list comprehension stores every result; a generator expression yields results lazily and can be consumed once.

| Readings | Loop (s) | Comprehensions (s) | map/filter (s) | Identical outputs |
|---:|---:|---:|---:|:---:|
| 10,000 | 0.000858 | 0.001072 | 0.001403 | Yes |
| 100,000 | 0.008881 | 0.010831 | 0.014293 | Yes |
| 1,000,000 | 0.090034 | 0.110826 | 0.148253 | Yes |

All are O(n) time. The explicit loop was fastest here, so a comprehension is not always the fastest or clearest choice. The list result used **85,176 bytes** for its container; the generator object used **216 bytes** (both exclude referenced float values). A generator expression such as `sum(c for c in readings if -50 <= c <= 50)` uses O(1) auxiliary space for the stream while a materialized list uses O(n); if multiple output lists are required, lists or multiple passes may still be necessary.

## Q6 Nested data Railway timetable

The timetable maps train number to a dictionary containing a display name, a list of `(station, arrival, departure)` tuples, and a set of running days. A station index maps station name to candidate train/stop/day records. The departure time of the third station is `timetable[train_no]["stops"][2][2]`. Dictionaries support train-number and station lookup; lists preserve stop order; tuples keep each stop record together; sets support average O(1) weekday checks.

For Monday at Katpadi the program returned trains sorted by departure: Southern Mail 07:10, City Link 07:35, Coastal Express 08:05. An unknown station returned no trains. A Sunday query excluded trains not running Sunday. The full sample timetable prints train name, days, and stops.

| Trains | Index build (s) | Scan query (s) | Indexed query (s) | Shallow index bytes | Equal results |
|---:|---:|---:|---:|---:|:---:|
| 100 | 0.000016 | 0.000007 | 0.000001 | 3,398 | Yes |
| 1,000 | 0.000173 | 0.000075 | 0.000011 | 25,862 | Yes |
| 10,000 | 0.002286 | 0.000733 | 0.000160 | 251,846 | Yes |

Without an index, one query may inspect every stop: O(total stops). With a station index it examines only the station's candidate trains, O(trains at that station), plus weekday checks. Building the index takes O(total stops) time and uses O(total stops) additional references; the reported memory is shallow container size and does not include referenced strings/records. For a single small schedule, scanning can be simpler; repeated queries justify the index. A flat list alternative also requires O(total stops) per query unless sorted/indexed first.

## Q7 Contact merging from first principles

### Requirements and design

Inputs are contact records from multiple devices; output is one grouped contact with all display names, normalized phone numbers, and email addresses. Records with the same normalized ten-digit phone merge. Phone normalization strips punctuation and spaces, removes a leading Indian `91` from a 12-digit number, and accepts only ten digits. Names are case-folded, punctuation removed, and common titles dropped for a normalized-name set, while original display spellings are retained. Phone number is the primary dictionary key; a normalized email is a fallback only when phone is absent. If both are absent, records are kept separate because there is no reliable identity evidence. Same-name contacts with different phone numbers remain separate.

Pseudocode: for each record, normalize phone and email; choose `phone:<digits>`, else `email:<address>`, else a unique record key; create a group if needed; add display and normalized name, valid number, and normalized email to sets. The implementation keeps all associated values in sets so duplicates collapse.

### Results and scale evidence

The six-record hand example merges the two “Ravi” records under `9840012345`, combines two Maya records under `9000011111`, keeps an email-only record, and keeps an unidentified record separate. Same-name “Alex” records with different phone numbers produce two groups.

| Contacts | Dictionary merge (s) | Pairwise merge (s) | Comparisons made | Pairwise estimate (s) |
|---:|---:|---:|---:|---:|
| 1,000 | 0.001944 | 0.007315 | 260,798 | 0.014 (estimated full-pair cost) |
| 100,000 | 0.287056 | Not run | 4,999,950,000 worst-case pairs | 140.3 (extrapolated) |

The 100,000-contact pairwise result is an extrapolation from the observed pairwise comparison cost, not an executed timing; the 100,000-record dictionary result is measured. It would require billions of pair checks to directly run the quadratic version. A dictionary performs O(n) average inserts/lookups and uses O(n) space for groups; pairwise comparisons take O(n²) time and O(n) group storage. The measured dictionary pass handled 100,000 records in about 0.29 seconds in this run. Its remaining limitation is identity quality: two people sharing a phone number will merge, while records with no phone or email cannot be confidently matched. A safer production tool would flag uncertain matches for review rather than infer identity from a similar name.

## Submission checklist

The required repository name is `CSA08-[RegisterNumber]-Assignment3`. Replace the placeholders on the report cover and README, create the GitHub repository, commit each task progressively, and share it with the faculty. Add execution screenshots to the task folders if required by your instructor; current task folders include text output captures. Submit the report PDF through the course portals yourself.
