import sys
import json
import duckdb

path = sys.argv[1]
with open(path) as f:
    assignments = json.load(f)  # list of [id, topic]

con = duckdb.connect("md:")
con.sql("USE webinar_research")
con.executemany("UPDATE posts SET topic = ? WHERE id = ?", [(t, i) for i, t in assignments])

from collections import Counter
counts = Counter(t for _, t in assignments)
print(f"Applied {len(assignments)} tags.")
for topic, n in counts.most_common():
    print(f"  {topic}: {n}")
