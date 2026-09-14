import duckdb

con = duckdb.connect('md:')
con.sql("CREATE DATABASE IF NOT EXISTS webinar_research")
con.sql("USE webinar_research")

con.sql("""
CREATE TABLE IF NOT EXISTS posts (
    id VARCHAR,
    source VARCHAR,
    era VARCHAR,
    type VARCHAR,
    date TIMESTAMP,
    title VARCHAR,
    url VARCHAR,
    text VARCHAR,
    points BIGINT,
    num_comments BIGINT,
    author VARCHAR
)
""")

# Load the 1,896 recent HN API items
con.sql("""
INSERT INTO posts
SELECT
    objectID AS id,
    'hn_api' AS source,
    'recent' AS era,
    type,
    CAST(created_at AS TIMESTAMP) AS date,
    title,
    url,
    coalesce(story_text, comment_text) AS text,
    points,
    num_comments,
    author
FROM read_json_auto('data/hn_duckdb_motherduck_last12mo.json')
""")

# Load the 377 matching rows from the 2022 sample dataset
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
