import duckdb

con = duckdb.connect('md:')
con.sql("USE webinar_research")

con.sql("""
INSERT INTO posts
SELECT
    CAST(id AS VARCHAR) AS id,
    'hn_sample' AS source,
    '2022' AS era,
    type,
    timestamp AS date,
    title,
    url,
    text,
    score AS points,
    descendants AS num_comments,
    "by" AS author
FROM sample_data.hn.hacker_news
WHERE lower(coalesce(title,'')) LIKE '%duckdb%' OR lower(coalesce(title,'')) LIKE '%motherduck%'
   OR lower(coalesce(text,'')) LIKE '%duckdb%' OR lower(coalesce(text,'')) LIKE '%motherduck%'
   OR lower(coalesce(url,'')) LIKE '%duckdb%' OR lower(coalesce(url,'')) LIKE '%motherduck%'
""")

print("--- counts by era and type ---")
for row in con.sql("""
    SELECT era, type, count(*) AS n
    FROM posts
    GROUP BY era, type
    ORDER BY era, type
""").fetchall():
    print(row)

print()
print("--- total row count ---")
print(con.sql("SELECT count(*) FROM posts").fetchall())
