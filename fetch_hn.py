import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta
from collections import Counter

END = datetime(2026, 9, 11, 23, 59, 59, tzinfo=timezone.utc)
START = END - timedelta(days=365)

QUERIES = ["duckdb", "motherduck"]
FIELDS = ["objectID", "type", "created_at", "title", "url",
          "story_text", "comment_text", "points", "num_comments", "author"]

BASE = "https://hn.algolia.com/api/v1/search_by_date"
MAX_RETRIEVABLE = 1000  # Algolia HN API caps page*hitsPerPage results per query

def month_chunks(start, end):
    chunks = []
    cur = start
    while cur < end:
        # next month boundary
        if cur.month == 12:
            nxt = cur.replace(year=cur.year + 1, month=1)
        else:
            nxt = cur.replace(month=cur.month + 1)
        chunk_end = min(nxt, end + timedelta(seconds=1)) - timedelta(seconds=1)
        chunks.append((cur, min(chunk_end, end)))
        cur = nxt
    return chunks

def api_call(query, start_ts, end_ts, page, hits_per_page=1000):
    params = {
        "query": query,
        "tags": "(story,comment)",
        "numericFilters": f"created_at_i>={start_ts},created_at_i<={end_ts}",
        "typoTolerance": "false",
        "hitsPerPage": hits_per_page,
        "page": page,
    }
    url = BASE + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def fetch_range(query, start_dt, end_dt, label):
    start_ts, end_ts = int(start_dt.timestamp()), int(end_dt.timestamp())
    first = api_call(query, start_ts, end_ts, page=0)
    nb_hits = first["nbHits"]
    results = list(first["hits"])
    if nb_hits > MAX_RETRIEVABLE:
        # split this range in half and recurse
        mid = start_dt + (end_dt - start_dt) / 2
        print(f"    [{label}] nbHits={nb_hits} exceeds cap, splitting at {mid.isoformat()}")
        left = fetch_range(query, start_dt, mid, label + "a")
        right = fetch_range(query, mid + timedelta(seconds=1), end_dt, label + "b")
        return left + right
    else:
        page = 1
        while len(results) < nb_hits:
            data = api_call(query, start_ts, end_ts, page=page)
            if not data["hits"]:
                break
            results.extend(data["hits"])
            page += 1
        print(f"    [{label}] {start_dt.date()} to {end_dt.date()}: nbHits={nb_hits} fetched={len(results)}")
        return results

all_hits = {}
for q in QUERIES:
    print(f"Fetching results for query: {q}")
    for i, (cstart, cend) in enumerate(month_chunks(START, END)):
        label = f"{q}:{cstart.strftime('%Y-%m')}"
        hits = fetch_range(q, cstart, cend, label)
        for h in hits:
            all_hits[h["objectID"]] = h
        time.sleep(0.15)

print(f"\nTotal unique items after merge/dedupe: {len(all_hits)}")

def get_type(h):
    tags = h.get("_tags", [])
    for t in tags:
        if t in ("story", "comment"):
            return t
    return h.get("type")

items = []
for h in all_hits.values():
    item = {f: h.get(f) for f in FIELDS if f != "type"}
    item["type"] = get_type(h)
    # reorder to match requested field order
    item = {f: item.get(f) for f in FIELDS}
    items.append(item)

items.sort(key=lambda x: x.get("created_at") or "")

with open("data/hn_duckdb_motherduck_last12mo.json", "w") as f:
    json.dump(items, f, indent=2)

stories = [i for i in items if i["type"] == "story"]
comments = [i for i in items if i["type"] == "comment"]
other = [i for i in items if i["type"] not in ("story", "comment")]

month_counts = Counter()
for i in items:
    if i.get("created_at"):
        month_counts[i["created_at"][:7]] += 1

print(f"\nSaved {len(items)} items to data/hn_duckdb_motherduck_last12mo.json")
print(f"Stories: {len(stories)}  Comments: {len(comments)}  Other/unknown: {len(other)}")
print("\nPer-month counts:")
for month in sorted(month_counts):
    print(f"  {month}: {month_counts[month]}")

with open("data/summary.json", "w") as f:
    json.dump({
        "total": len(items),
        "stories": len(stories),
        "comments": len(comments),
        "per_month": dict(sorted(month_counts.items())),
        "date_range": {"start": START.isoformat(), "end": END.isoformat()},
    }, f, indent=2)
