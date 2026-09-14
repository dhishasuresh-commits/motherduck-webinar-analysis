# Webinar topic analysis

Research for a growth marketing job application at MotherDuck: what should
the next webinar be about, based on what people actually say about DuckDB
and MotherDuck on Hacker News — not on what seems intuitively hot.

Full methodology, corpus provenance, and rerun instructions are in
[README.md](README.md). This document is the findings.

## The headline number, with its caveat attached

Raw mention volume: 377 (2022, 314-day window) vs. 1,896 (recent, 364-day
window). Normalized to a daily rate, that's a **~4.3x increase** — notably
less than the naive 5.0x you get from dividing the raw counts, because the
2022 window is about six weeks shorter.

That 4.3x number still isn't a clean "DuckDB interest grew 4.3x" claim: this
project has no all-of-Hacker-News baseline for either window, so there's no
way to separate DuckDB/MotherDuck-specific growth from Hacker News' overall
post/comment volume growing since 2022 for unrelated reasons. Treat the
raw-volume comparison as directional, not a rate.

**The finding that does hold up under that scrutiny is the topic-mix shift**
within each corpus — a share-of-mentions comparison, which isn't affected by
how much bigger HN got in the meantime.

## Topic mix: 2022 vs. recent

| Topic | 2022 | Recent | Change |
|---|---:|---:|---:|
| AI agents and MCP | 0 (0.0%) | 165 (8.7%) | **+8.7pp** |
| DuckLake and lakehouse formats | 6 (1.6%) | 115 (6.1%) | +4.5pp |
| customer-facing and embedded analytics | 2 (0.5%) | 42 (2.2%) | +1.7pp |
| performance and benchmarks | 65 (17.2%) | 352 (18.6%) | +1.3pp |
| cost and pricing vs other warehouses | 2 (0.5%) | 35 (1.8%) | +1.3pp |
| Postgres integration | 25 (6.6%) | 82 (4.3%) | −2.3pp |
| local vs cloud execution | 63 (16.7%) | 241 (12.7%) | −4.0pp |
| general or other | 173 (45.9%) | 790 (41.7%) | −4.2pp |
| Python and notebook workflows | 41 (10.9%) | 74 (3.9%) | **−7.0pp** |

Two things worth building a narrative around:

- **AI agents/MCP is the only topic that went from non-existent to
  top-4.** It didn't exist as a category in 2022 (MCP itself wasn't
  invented yet) and is now the 4th-largest theme.
- **Python/notebook workflows fell the hardest**, in both share and
  framing. In 2022 people talked about DuckDB mainly as "a faster
  replacement for Pandas." That framing has been crowded out — not
  necessarily because it stopped being true, but because newer narratives
  (agents, DuckLake, the Aug 2026 AWS/DuckLabs acquisition) now dominate
  the conversation.

"General or other" (41.7% of recent mentions) is itself a real finding, not
noise to explain away — see the cluster breakdown below.

## What "general or other" actually contains

790 recent items didn't fit any of the 8 themes. Read and clustered (not
re-tagged) into:

| Cluster | Count |
|---|---:|
| General diffuse DuckDB chatter (capability Qs, tooling asides, personal-project mentions) | 551 |
| AWS acquires DuckLabs — reaction & governance debate (Aug 2026 news cycle) | 62 |
| Unrelated hiring-thread noise (job ads swept in by keyword search) | 50 |
| Short one-line praise or complaints | 38 |
| Official DuckDB/MotherDuck blog & docs pages, no distinct theme | 32 |
| Niche extension & side-project Show HN launches (DuckDB incidental) | 32 |
| Architecture/capability comparison Q&A (OLAP vs OLTP, "how does X compare") | 25 |

Roughly 15% of this bucket (job ads + incidental Show HN mentions) is pure
keyword-search noise, not really about DuckDB. The acquisition-reaction spike
is a one-time news event. The ~70% "diffuse chatter" remainder is the honest
ceiling on how much of this corpus doesn't map to a specific webinar theme
even after real reading.

## What people are building

Searched the recent corpus for build-narrative language ("Show HN," "I
built," "we use DuckDB for," architecture descriptions): **221 items**
describe an actual build.

| What they built | Count |
|---|---:|
| Data pipelines / warehouses / ETL replacements | 47 |
| AI agent / MCP tooling | 47 |
| Browser/WASM query & analytics tools | 41 (36 after removing 2 mismatches, 2 duplicates, 1 non-build) |
| Other (one-off tools, personal projects) | 53 |
| Logging / monitoring / observability tools | 10 |
| DuckDB extensions (community add-ons) | 9 |
| Niche vertical apps (finance/trading, spatial, hobby) | 8 |
| Dev tooling: SQL clients, CLIs, GUIs, transpilers | 6 |

Ranking by how much detail builders wrote about their own project (not by
popularity) surfaces AI-agent tooling almost exclusively — 15 of the top 20
most-detailed build write-ups are agent/MCP launches. That's a real signal
about who's building in public around DuckDB right now, not a ranking
artifact.

### Browser/WASM deep dive

Of the 36 genuine browser/WASM builds, the dominant pattern is **"drop a
file in, query it with SQL, nothing leaves the browser"** — SQL IDEs,
embeddable analytics components, and niche domain viewers (chip-testing
yield data, clinical trial file formats, Wikidata). Consistently reported
problems:

1. **No feature parity with native DuckDB** — one team built DuckDB-WASM +
   Parquet + S3, then "ended up stripping it all out and replacing it with
   a boring REST API" over missing compression support. A DuckDB
   maintainer confirmed: *"the wasm docs state that feature-parity isn't
   there — yet."*
2. **No multithreading or SIMD in the browser**, reported as making CSV
   parsing "painfully slow" vs. native.
3. **Unreliable persistent storage** — OPFS-backed writes surviving a
   reload "isn't really reliable," with real risk of silent data loss on
   storage eviction.
4. **Bundle size** — cited figures range from ~6MB compressed to 95MB+.

## What people are stuck on

Searched for question-phrased and stuck/confused/limitation language:
**~230 genuine questions** (of 367 pattern-matched candidates, after
filtering out rhetorical asides and acquisition-news commentary).

| What they were trying to do | Count (approx.) |
|---|---:|
| "Should I use DuckDB or X?" — comparison/decision questions | ~75 |
| Postgres integration how-to (pg_duckdb, pg_lake, FDW, catalogs) | ~28 |
| Concurrency / multi-writer / server & hosting | ~24 |
| Memory, OOM & scaling limits | ~16 |
| DuckLake / Iceberg / table-format specifics | ~14 |
| Browser/WASM technical questions | ~12 |
| Vector search (VSS/HNSW) capability questions | ~7 |
| Conceptual/architecture clarification | ~15 |
| Everything else (one-off/niche) | ~39 |

**The single dominant unmet need isn't a technical limitation at all** —
it's people trying to figure out whether DuckDB is the right tool relative
to something they already know: Postgres, Pandas, ClickHouse, Snowflake.
That's a positioning gap, not a product gap.

## Cross-referenced against MotherDuck's own event history

`data/covered-topics.csv` — 243 MotherDuck events, Dec 2023 to present —
lets us check which of these themes are already saturated vs. genuine
whitespace, instead of guessing:

| Theme | HN signal | Events already run | Read |
|---|---:|---:|---|
| AI agents / MCP | 165 mentions, 47 builds, biggest mover (+8.7pp) | **55 events** | Saturated. Don't pitch "AI agents 101" — go narrower if pitching this at all. |
| DuckLake / lakehouse | 115 mentions, +4.5pp | 21 events | Well covered, matches MotherDuck's own product push. |
| "DuckDB vs. X" decision framework | **~75 questions** — the single largest need signal in the whole dataset | **0 dedicated events** | **Clear whitespace.** Nothing in 243 events directly addresses "when do I use DuckDB vs. Postgres/Pandas/Snowflake/ClickHouse." |
| Postgres integration | 107 mentions across both categories and questions | 7 events | Underserved relative to organic interest — it's a top-3 specific theme in the recent corpus. |
| Browser/WASM & embedded analytics | 36 real builds + 42 "customer-facing" mentions | 4–5 events | Underserved relative to grassroots building activity. |
| Cost/pricing vs. other warehouses | 37 mentions, but includes high-engagement outliers ("$2M/yr on Snowflake," "OpenAI Just Made Analytics 10x Cheaper") | 6 events | Moderate coverage; individual items suggest more appetite than volume alone implies. |

## Recommendation

The best-supported pitch, in order:

1. **"DuckDB vs. X: a decision framework"** (Postgres, Pandas, Snowflake,
   ClickHouse) — addresses the single largest recurring need (~75
   questions) and is genuine whitespace against 243 prior events. Could
   fold in the Postgres-integration how-to questions (~28) as a segment,
   since "should I use DuckDB with my Postgres setup" is itself one of the
   most common comparison questions.
2. **Embedding DuckDB in your own product (browser/WASM + customer-facing
   analytics)** — grounded in 36 real community builds and clear gaps
   (feature parity, storage reliability, bundle size) worth addressing
   head-on, with only a handful of prior events on the topic.
3. If pitching AI agents/MCP at all, don't compete on "what is MCP" — that
   ground is covered 55 times over. A defensible angle is the honest one
   this dataset surfaces: DuckDB used *as infrastructure inside* an agent
   tool (47 builds do this), not "agents as a feature of DuckDB."

## Data files

| File | What it is |
|---|---|
| `data/hn_duckdb_motherduck_last12mo.json` | Raw recent-corpus scrape (1,896 items) |
| `data/relevance_check.csv` | 50-item stratified relevance sample + labels |
| `data/summary.json` | Fetch-run metadata (counts, date range, per-month breakdown) |
| `data/covered-topics.csv` | MotherDuck's own event history (243 rows), used for the whitespace cross-reference above |

The tagged `posts` table itself lives in MotherDuck, not as a file in this
repo — see README.md for the schema and how to query it.
