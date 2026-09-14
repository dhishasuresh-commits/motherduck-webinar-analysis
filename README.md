# MotherDuck webinar topic research

Comparing what people actually say about DuckDB and MotherDuck on Hacker News
today against a 2022 baseline, to find topics worth building a webinar around.
Built as part of research for a growth marketing job application at
MotherDuck.

## What's here

Two corpora of Hacker News stories and comments that mention "duckdb" or
"motherduck", loaded into one table (`webinar_research.posts`) in a MotherDuck
database, with every row hand-tagged into one of 8 topics (or "general or
other") based on what it's actually about — not keyword-matched.

| era | source | count | date range |
|---|---|---|---|
| `2022` | MotherDuck's shared `sample_data.hn.hacker_news` table | 377 (326 comments, 51 stories) | Jan–Nov 2022 |
| `recent` | Algolia HN Search API | 1,896 (1,487 comments, 409 stories) | last 12 months |

Headline finding: mention volume is up ~5x, and "AI agents and MCP" went from
a topic that didn't exist in 2022 to the 4th-largest theme in the recent
corpus. Full topic breakdown lives in the `posts` table (see queries below).

## Where the two corpora came from

**2022 baseline** — `sample_data.hn.hacker_news` is a shared sample dataset
every MotherDuck account can query. It only covers Jan–Nov 2022. We filtered
it to rows where the title, text, or URL contains "duckdb" or "motherduck"
(case-insensitive substring match) — see the `WHERE` clause in
`load_sample_data.py`. That gave exactly 377 rows, matching the 326/51
comment/story split used as the starting reference point for this project.

**Recent corpus** — pulled fresh from the free
[Algolia HN Search API](https://hn.algolia.com/api) (no key needed) by
`fetch_hn.py`, searching for "duckdb" and "motherduck" separately across
stories and comments from the last 12 months, then deduping by HN's
`objectID`. Two non-obvious things the script works around:

- The OR-tag syntax needs parentheses (`tags=(story,comment)`) — a bare comma
  is read as AND, which silently returns zero results.
- The API caps any single query at ~1,000 retrievable results regardless of
  the reported `nbHits`. `fetch_hn.py` chunks the fetch by month (and
  recursively splits further if a single month would still exceed the cap)
  so nothing gets silently dropped.

Typo-tolerance is turned off, since by default Algolia's fuzzy matching pulls
in unrelated terms like "Duck.ai" and "DuckDuckGo."

## How the relevance check worked

Before trusting the "recent" corpus, we stratified-sampled 50 items
(proportional to the real 409/1,896 story/comment split → 11 stories, 39
comments) into `data/relevance_check.csv`, with a `keyword_context` column
(200 characters either side of the first "duckdb"/"motherduck" match) and a
`full_length` column, so a reviewer could judge relevance without reading the
full text of every row.

`label.py` is a small resumable CLI: it shows one row at a time (date, type,
title, keyword context), takes `1`/`0`/`s`, and saves the whole CSV back to
disk after every answer so it's safe to quit anytime. It computes precision —
overall, and split by story vs. comment — once every row has an answer.

Two of the 50 rows initially came back with an empty `keyword_context`
because the match was in the story's URL rather than its title or body (HN
stories can be title/URL-only, with no text at all). Adding a `url` column
and re-labeling those two against the URL brought:

- Overall precision: 40/50 = **80.0%**
- Story precision: 10/11 = **90.9%**
- Comment precision: 30/39 = **76.9%**

## How the topic tagging worked

Each row in `posts` has a `topic` column, one of:

`Postgres integration` · `cost and pricing vs other warehouses` ·
`AI agents and MCP` · `DuckLake and lakehouse formats` ·
`customer-facing and embedded analytics` · `Python and notebook workflows` ·
`performance and benchmarks` · `local vs cloud execution` ·
`general or other`

**First attempt (`tag_topics.py`) was keyword/regex-based** — priority-ordered
patterns matched against title+text+url — and got 50.8% of rows dumped into
"general or other." That's a proxy, not judgment: it can't tell that a
comment about "concurrency limits" or "ingestion rates" is really about
performance, and can't weigh title/text/url together the way a human would.
The script is kept in this repo for the record, but **it is not how the final
tags were produced.**

**Final tags were applied by actually reading every row**, in 23 batches of
~100. For each batch: `fetch_batch.py` pulled a compact pipe-delimited dump
(id/type/title/url/text) from MotherDuck; each row's title, text, and URL
were read and judged individually; the resulting `[id, topic]` assignments
were written to a JSON file and applied with `apply_batch.py`. This is why
the two scripts take an offset/limit and a JSON file, respectively, rather
than doing the whole table in one shot — the judgment step happens by hand,
in between.

Final overall "general or other" rate: **42.4%** (963/2,273) — still high,
but now a genuine finding rather than a classifier blind spot: a large share
of organic HN chatter about DuckDB really is generic praise, tooling asides,
job-posting noise, and reactions to the August 2026 AWS/DuckLabs acquisition
news, none of which maps to a specific webinar theme.

## What each script does

| Script | Does |
|---|---|
| `fetch_hn.py` | Pulls the last-12-months corpus from the Algolia HN API, chunked by month, deduped, written to `data/hn_duckdb_motherduck_last12mo.json` and `data/summary.json`. |
| `load_motherduck.py` | Connects to MotherDuck, creates the `webinar_research` database and `posts` table, and loads **both** the recent HN-API JSON and the matching 2022 `sample_data.hn.hacker_news` rows. |
| `load_sample_data.py` | Standalone re-run of just the 2022-sample insert (the second half of `load_motherduck.py`) — kept from when the two loads were debugged separately. Only needed if you already have the recent data loaded and just need the 2022 rows (re)inserted. |
| `label.py` | Interactive, resumable relevance-labeling CLI for `data/relevance_check.csv`. Prints precision (overall, story, comment) once every row is labeled. |
| `tag_topics.py` | The original keyword-based topic classifier. Superseded — see above — kept for reference. |
| `fetch_batch.py <offset> <limit>` | Prints one batch of `posts` rows as compact pipe-delimited text, for manual reading. |
| `apply_batch.py <assignments.json>` | Applies a hand-written `[[id, topic], ...]` JSON file to the `posts.topic` column and prints a per-topic tally for that batch. |

## Rerunning this

**Prerequisites:**
- Python 3 with the `duckdb` package (`pip3 install duckdb`)
- A MotherDuck account
- The `motherduck_token` environment variable set in your shell profile
  (specifically `~/.zshenv` if you're on zsh, not `~/.zshrc` — `.zshrc` only
  loads for interactive shells, and non-interactive script runs need
  `.zshenv`). Get a token from the MotherDuck UI under Settings → Access
  Tokens. Never commit it or pass it on the command line — every script here
  connects with `duckdb.connect("md:")`, no argument, so it's picked up
  silently from the environment.

**To rebuild the recent corpus from scratch:**

```bash
# fetch_hn.py hardcodes today's date as the end of the 12-month window —
# update the END constant near the top of the file first if you want a
# fresh window rather than the original Sep 2025–Sep 2026 one.
python3 fetch_hn.py
```

**To load everything into MotherDuck:**

```bash
python3 load_motherduck.py
```

This creates the `webinar_research` database (if it doesn't exist), creates
`posts`, and inserts both eras. It does **not** check for existing rows —
rerunning it against a database that already has data will duplicate rows.
If you need to start over, drop the table first (`DROP TABLE posts;` from a
DuckDB/MotherDuck shell) or work in a fresh database name.

**To redo the relevance check:**

```bash
python3 label.py
```

**To redo the topic tagging properly (i.e., not with `tag_topics.py`):**

There's no single script for this — it's inherently a manual loop. Roughly:

```bash
python3 fetch_batch.py 0 100        # read the output
# write the 100 [id, topic] judgments to a JSON file
python3 apply_batch.py batch.json   # repeat with offset 100, 200, ... until done
```

**Useful queries once everything's loaded:**

```sql
-- topic breakdown by era, with each topic's share of its era
SELECT era, topic, count(*) AS n,
       count(*) * 100.0 / sum(count(*)) OVER (PARTITION BY era) AS pct
FROM posts GROUP BY era, topic ORDER BY era, n DESC;
```
