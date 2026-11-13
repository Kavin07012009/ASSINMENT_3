"""Q7: Contact merging by normalized phone, with email fallback and benchmarks."""
import random
import statistics
import string
import time


def normalize_phone(raw):
    if not raw:
        return ""
    digits = "".join(ch for ch in raw if ch.isdigit())
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    return digits if len(digits) == 10 else ""


def normalize_email(raw):
    return (raw or "").strip().casefold()


def normalize_name(raw):
    text = (raw or "").casefold().translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    while words and words[0] in {"dr", "mr", "mrs", "ms", "prof"}:
        words.pop(0)
    return " ".join(words)


def contact_key(contact, index):
    phone = normalize_phone(contact.get("phone"))
    if phone:
        return "phone:" + phone
    email = normalize_email(contact.get("email"))
    if email:
        return "email:" + email
    # With no stable identifier, do not guess that two records are the same.
    return f"unmatched-record:{index}"


def merge_contacts(contacts):
    merged = {}
    for i, contact in enumerate(contacts):
        key = contact_key(contact, i)
        entry = merged.setdefault(key, {"names": set(), "normalized_names": set(), "numbers": set(), "emails": set()})
        name = contact.get("name", "").strip()
        phone = normalize_phone(contact.get("phone"))
        email = normalize_email(contact.get("email"))
        if name:
            entry["names"].add(name)
            entry["normalized_names"].add(normalize_name(name))
        if phone:
            entry["numbers"].add(phone)
        if email:
            entry["emails"].add(email)
    return merged


def pairwise_merge(contacts):
    """Quadratic reference implementation; compares each record with prior records."""
    groups = []
    comparisons = 0
    for i, contact in enumerate(contacts):
        phone = normalize_phone(contact.get("phone"))
        email = normalize_email(contact.get("email"))
        match = None
        for group in groups:
            comparisons += 1
            if (phone and phone in group["numbers"]) or (not phone and email and email in group["emails"]):
                match = group
                break
        if match is None:
            match = {"names": set(), "normalized_names": set(), "numbers": set(), "emails": set()}
            groups.append(match)
        name = contact.get("name", "").strip()
        if name:
            match["names"].add(name)
            match["normalized_names"].add(normalize_name(name))
        if phone: match["numbers"].add(phone)
        if email: match["emails"].add(email)
    return groups, comparisons


def generate_contacts(n, seed=78):
    rng = random.Random(seed)
    contacts=[]
    distinct=max(1, n // 2)
    for i in range(n):
        person=i % distinct
        digits=f"984{person:07d}"[-10:]
        phone=f"+91 {digits[:5]} {digits[5:]}" if i % 2 == 0 else f"{digits[:5]}-{digits[5:]}"
        names=[f"Dr. Ravi {person}", f"ravi kumar {person}"]
        contacts.append({"name": names[i % 2], "phone": phone,
                         "email": f"ravi{person}@example.org" if i % 3 else ""})
    # Add occasional records with a missing phone; email provides the fallback key.
    for i in range(0, n, max(1, n // 100)):
        contacts[i]["phone"] = ""
    rng.shuffle(contacts)
    return contacts


def median_time(fn, data, repeats=3):
    samples=[]
    for _ in range(repeats):
        start=time.perf_counter(); result=fn(data); samples.append(time.perf_counter()-start)
    return statistics.median(samples), result


def main():
    small = [
        {"name": "Dr. Ravi", "phone": "+91 98400 12345", "email": "RAVI@example.com"},
        {"name": "ravi kumar", "phone": "9840012345", "email": "ravi.work@example.com"},
        {"name": "Maya", "phone": "90000-11111", "email": ""},
        {"name": "Maya alternate", "phone": "9000011111", "email": "maya@example.com"},
        {"name": "Email Only", "phone": "", "email": "only@example.com"},
        {"name": "", "phone": "", "email": ""},
    ]
    print("small merged by number:", merge_contacts(small))
    groups, comparisons = pairwise_merge(small)
    print("hand-check groups/comparisons:", len(groups), comparisons)
    print("same name different phones remain separate:", len(merge_contacts([
        {"name":"Alex","phone":"9000011111"},{"name":"Alex","phone":"9000022222"}])))
    print("n,dictionary_s,pairwise_measured_s,pairwise_comparisons,pairwise_projected_s")
    pairwise_1000 = None
    comparisons_1000 = None
    for n in (1_000, 100_000):
        contacts=generate_contacts(n)
        dict_s, result=median_time(merge_contacts, contacts)
        if n == 1_000:
            pair_s, pair_result=median_time(pairwise_merge, contacts, repeats=1)
            pairwise_1000=pair_s
            _, comparisons=pair_result
            comparisons_1000 = comparisons
            projection=pair_s * (n * (n - 1) / 2) / max(1, comparisons)
            assert len(result) == len(pair_result[0])
            print(f"{n},{dict_s:.6f},{pair_s:.6f},{comparisons},{projection:.3f}")
        else:
            comparisons=n*(n-1)//2
            projection=pairwise_1000*(n*(n-1)/2)/max(1, comparisons_1000)
            print(f"{n},{dict_s:.6f},not_run,{comparisons},{projection:.1f}")
    print("The 100000-contact pairwise value is an extrapolation from the observed pairwise comparison cost, not an executed timing.")


if __name__ == "__main__":
    main()
