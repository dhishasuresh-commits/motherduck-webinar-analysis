import sys
import duckdb

offset = int(sys.argv[1])
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100

con = duckdb.connect("md:")
con.sql("USE webinar_research")

rows = con.sql(f"""
    SELECT id, type, title, url, text
    FROM posts
    ORDER BY id
    LIMIT {limit} OFFSET {offset}
""").fetchall()

for row_id, typ, title, url, text in rows:
    title = (title or "").replace("\n", " ").replace("|", "/")
    url = (url or "")
    text = (text or "").replace("\n", " ").replace("|", "/")
    if len(text) > 350:
        text = text[:350] + "..."
    print(f"{row_id}|{typ}|{title}|{url}|{text}")
