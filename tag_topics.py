import re
import duckdb

TOPICS = [
    "Postgres integration",
    "cost and pricing vs other warehouses",
    "AI agents and MCP",
    "DuckLake and lakehouse formats",
    "customer-facing and embedded analytics",
    "Python and notebook workflows",
    "performance and benchmarks",
    "local vs cloud execution",
    "general or other",
]

# Priority-ordered rules: first matching rule wins. Each pattern is matched
# case-insensitively against title + text + url combined.
RULES = [
    ("DuckLake and lakehouse formats", [
        r"\bducklake\b", r"\biceberg\b", r"\bdelta ?lake\b", r"\bhudi\b",
        r"\blakehouse\b", r"\btable format\b",
    ]),
    ("AI agents and MCP", [
        r"\bmcp\b", r"model context protocol", r"\bcoding agent", r"\bai agent",
        r"\bagentic\b", r"\bllm\b", r"\bllms\b", r"\bclaude\b", r"\bchatgpt\b",
        r"\bgpt-?4\b", r"\bcopilot\b", r"\bcursor\b", r"\blangchain\b",
        r"\bautogen\b", r"\bcrewai\b", r"\bvibe.?cod",
    ]),
    ("Postgres integration", [
        r"\bpostgres\b", r"\bpostgresql\b", r"pg_duckdb", r"\bpsql\b",
        r"foreign data wrapper", r"\bsupabase\b", r"\bpglite\b",
    ]),
    ("cost and pricing vs other warehouses", [
        r"\bcost\b", r"\bpricing\b", r"\bprice\b", r"\bpriced\b", r"\bexpensive\b",
        r"\bcheaper\b", r"\bbilling\b", r"\btco\b", r"total cost of ownership",
        r"\$\d",
    ]),
    ("customer-facing and embedded analytics", [
        r"embedded analytics", r"embed analytics", r"customer-facing",
        r"customer facing", r"in-app analytics", r"white-label analytics",
        r"saas analytics", r"multi-tenant analytics",
    ]),
    ("Python and notebook workflows", [
        r"\bpython\b", r"\bpandas\b", r"\bjupyter\b", r"\bnotebook\b",
        r"\bpolars\b", r"\bdataframe\b", r"\bcolab\b", r"\bipynb\b",
    ]),
    ("performance and benchmarks", [
        r"\bbenchmark", r"\btpc-?h\b", r"\btpc-?ds\b", r"\bfaster\b",
        r"\bperformance\b", r"\bthroughput\b", r"\blatency\b",
        r"queries per second", r"rows per second", r"\bspeedup\b",
        r"billion rows?\b",
    ]),
    ("local vs cloud execution", [
        r"\bwasm\b", r"\bwebassembly\b", r"local-?first", r"\bserverless\b",
        r"runs? locally", r"single binary", r"\boffline\b", r"\bon-device\b",
        r"client-side", r"in.the.browser", r"\bedge\b",
    ]),
]


def classify(title, text, url):
    haystack = " ".join(x for x in [title or "", text or "", url or ""]).lower()
    for topic, patterns in RULES:
        for pat in patterns:
            if re.search(pat, haystack):
                return topic
    return "general or other"


def main():
    con = duckdb.connect("md:")
    con.sql("USE webinar_research")
    con.sql("ALTER TABLE posts ADD COLUMN IF NOT EXISTS topic VARCHAR")

    rows = con.sql("SELECT id, title, text, url FROM posts ORDER BY id").fetchall()
    print(f"Fetched {len(rows)} rows to classify.")

    total = len(rows)
    other_count = 0
    batch_size = 100

    for start in range(0, total, batch_size):
        batch = rows[start:start + batch_size]
        assignments = []
        for row_id, title, text, url in batch:
            topic = classify(title, text, url)
            if topic == "general or other":
                other_count += 1
            assignments.append((row_id, topic))

        con.executemany(
            "UPDATE posts SET topic = ? WHERE id = ?",
            [(topic, rid) for rid, topic in assignments],
        )

        done = min(start + batch_size, total)
        print(f"Batch {start//batch_size + 1}: tagged rows {start+1}-{done} "
              f"(running 'general or other' count: {other_count}/{done} = {other_count/done:.1%})")

    pct_other = other_count / total
    print()
    print(f"Final: {other_count}/{total} = {pct_other:.1%} tagged 'general or other'")

    if pct_other > 0.20:
        print("\n*** Exceeds 20% threshold — stopping before the era/topic summary. ***")
        print("\nSample of 'general or other' rows for review:")
        samples = con.sql("""
            SELECT era, type, title, url, left(text, 150) AS text_snippet
            FROM posts
            WHERE topic = 'general or other'
            ORDER BY random()
            LIMIT 15
        """).fetchall()
        for s in samples:
            print("---")
            print("era:", s[0], "| type:", s[1])
            print("title:", s[2])
            print("url:", s[3])
            print("text:", s[4])
    else:
        print("\nWithin threshold — proceeding to era/topic summary would be the next step.")


if __name__ == "__main__":
    main()
