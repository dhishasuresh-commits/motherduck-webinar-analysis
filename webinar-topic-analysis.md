# Three things I'd run at MotherDuck, and the data behind them

*Dhisha Suresh Babu | September 2026*

---

## What I found

I pulled every Hacker News post and comment mentioning DuckDB or MotherDuck from two periods: 2022, using MotherDuck's own `sample_data.hn.hacker_news` table, and the last twelve months, using the Algolia HN API. That gave me 2,273 items, which I loaded into MotherDuck and read item by item to assign topics. I then compared what people discuss against every event MotherDuck has run since December 2023, 243 in total.

Three things came out of it.

Performance and benchmarking is the largest single topic in both periods. MotherDuck's CEO has already argued that benchmarks can't be trusted, but no session has taken the next step: across 243 events, ClickHouse and Polars are never named, and DuckDB has never been put head-to-head against a competitor. DuckDB has become the engine that other engines benchmark themselves against, which means those evaluation conversations are already happening without MotherDuck in them.

Thirty-six people shipped browser-based DuckDB tools in the last twelve months, and they keep hitting the same four walls. The last time MotherDuck covered DuckDB in the browser was May 2024, over two years ago.

The single largest category of questions people ask, roughly 75 instances, is which tool to choose. That one is not a webinar. It is written comparison content, and it costs a fraction of a session.

---

## 1. Your CEO already said benchmarks lie. People still have to choose.

**Format:** Webinar, with an outside presenter. See the note below.

**The finding.** Performance and benchmarks is the largest specific topic in the corpus and the only one that is both large and stable: 17.2% of DuckDB discussion in 2022 and 18.6% in the last twelve months, 352 items. The highest-engagement items in the recent corpus are all benchmark content. DuckDB's own Async I/O post at 281 points, the sharded 1T-row challenge at 224, and a four-way Polars, DuckDB, Daft and Spark comparison at 263. Alongside those sits a cluster of posts from newer engines, SlothDB and Stratum among them, framed explicitly as beating DuckDB on ClickBench.

The observation worth building on: DuckDB has become the engine other engines benchmark themselves against. That is a strong position and an exposed one. Competitors choose the workload, and the evaluation conversation happens in threads where MotherDuck has no presence.

Thread: https://news.ycombinator.com/item?id=45920881

**What is already covered, and what isn't.** In October 2025, Jordan Tigani ran a livestream called "Lies, Damn Lies, and Benchmarks" on DuckDB performance and whether benchmarking techniques can be trusted at all. That argument is made, by the CEO, with a recording available. What no session has done is the next step. Across 243 events from December 2023 to November 2026, ClickHouse and Polars are never mentioned by name, and no session puts DuckDB head-to-head against a named competitor.

So the gap is not "are benchmarks reliable." It is "given that they are not, how do I actually decide." This session picks up where Tigani's left off and should reference it directly.

**Who's in the room.** An engineer choosing an analytical engine for a new project. They have already tried DuckDB, they have their own numbers, and they are looking for evidence and detail to justify a decision to their team.

**Why this session.** Run the same workload across engines, show where the numbers diverge, and be explicit about which differences matter for which workloads. The output is a decision framework, not a scoreboard.

**The credibility problem, and how to solve it.** MotherDuck running a comparison of DuckDB against ClickHouse and Polars is the vendor grading its own homework, and this audience will see that immediately. There is precedent in MotherDuck's own event history: the BI session used Ryan Dolley, an independent analyst, rather than an in-house voice. The same move applies here. This session needs a third-party presenter or an author of one of the competing engines to be worth running at all.

**Product tie-in.** The vs Snowflake, vs BigQuery, vs Redshift and vs ClickHouse comparison pages. This sends qualified traffic to pages that already exist.

**Promotion.** The benchmark threads themselves, plus the DuckDB newsletter and Slack community.

**Metric and guardrail.** Registrant-to-trial as the metric, since this audience is mid-evaluation. Show rate as the guardrail. One session is a single data point, so I would read it against the baseline across several rather than on its own.

---

## 2. Where the browser stops being enough

**Format:** Webinar, live build.

**The finding.** In the last twelve months, 36 people posted browser-based tools built on DuckDB-WASM. Almost all of them are the same shape: drop a file in, query it with SQL, nothing leaves the machine. Duck-UI, a browser SQL IDE, reached 213 points. A Citi Bike visualization rendering 291 million rides in the browser reached 113. Below those sits a long tail of general-purpose SQL workbenches, several openly competing with each other, plus domain viewers for chip-testing yield data, clinical trial formats and Wikidata.

They also keep hitting the same four walls.

- **Feature parity.** One team built on DuckDB-WASM with Parquet and S3, then stripped it out and replaced it with a REST API because capabilities they needed were missing from the WASM build. A DuckDB maintainer replied confirming that parity is not there yet.
- **No multithreading or SIMD** in the browser, which one builder said made CSV parsing painfully slow next to native.
- **Unreliable persistence.** OPFS survival across page reloads was described as not really reliable, with the risk that a browser evicts the origin's storage and silently drops unsynced writes.
- **Bundle size.** Cited figures ran from roughly 6MB compressed to over 95MB, a real cost for something meant to drop into a web page.

Duck-UI thread: https://news.ycombinator.com/item?id=45633453
The WASM-to-REST-API thread, with the maintainer's parity reply: https://news.ycombinator.com/item?id=45780399

**Who's in the room.** A developer who built or is building a browser-only analytical tool and has hit one of those four walls. They are not on MotherDuck. They chose the browser specifically to avoid a backend.

**Why this session.** Three of the four walls are reasons a browser-only build eventually needs something behind it. That makes the honest version of this talk more useful than an advocacy one: here is what DuckDB-WASM does well, here is exactly where it stops, and here is what you do at that point. Taking the limitations seriously is what earns this audience's trust.

**Coverage.** MotherDuck last covered DuckDB in the browser at Data @Scale in May 2024, over two years ago, when this was mostly a promising idea. Nothing since. Beyond Charts in March 2026 covers Dives, which are hosted React apps built on MotherDuck through an AI agent. That is the path for people already on the platform. These 36 are not on it yet.

**Product tie-in.** The core cloud product as the backend these builds end up needing, and Dives as the destination for the ones that want to stop maintaining their own UI.

**Promotion.** The Show HN threads themselves, several of which are still active, plus DuckDB Slack and the newsletter. This audience is unusually easy to find because they announced themselves.

**Metric and guardrail.** Registrant-to-signup as the metric, since this audience has a live problem and can act on it. Show rate as the guardrail. Same caveat on reading a single session.

**Confidence.** The 36 figure comes from a pattern-matched pass over the corpus, not the item-by-item read used for topic tagging. I removed two category mismatches, two duplicates and one item that referenced SQLite prior art rather than a DuckDB build. Treat it as a confident estimate rather than an exact census.

---

## 3. The 75 questions: comparison content, not a webinar

**Format:** Five written comparison pages.

**The finding.** I pulled every item in the recent corpus phrased as a question or a stuck point, roughly 230 after filtering. The largest group by a wide margin is comparison and decision questions, around 75 instances, more than double the next category. People asking whether to use DuckDB or Polars, or ClickHouse Local, or Postgres, or pandas, and why.

A representative sample:

- What is DuckDB better compared to, and what were people using before it?
- Why DuckDB when one can use Python and pandas?
- What's the advantage over Polars for the same task?
- Anyone tried both DuckDB and ClickHouse Local?
- Why did you use DuckDB instead of Snowflake?

**Why this is not a webinar.** These are not questions people attend a session to answer. They are questions people type into a search box or an AI assistant at the moment of deciding. The right format is written comparison content, which costs a fraction of a webinar and compounds rather than expiring.

**Why it matters commercially.** Every one of those 75 is a query that will be asked again next month, and the answer is currently being written by whoever ranks for it. Separately, three of the 50 items in my hand-labelled sample were people confused about the relationship between DuckDB, the DuckDB Foundation and MotherDuck. If third parties are supplying the answers to comparison questions, they are also supplying the answers to ownership and architecture questions.

**One thing the data says that I did not expect.** Cost and pricing versus other warehouses is only 1.8% of recent discussion, 35 items. People are not comparing these tools on price. They are comparing on fit: what is this for, when does it break, what do I lose. Comparison content built around price would miss what is actually being asked.

**What I would do.** Take the top five comparisons by question volume and write one honest page each, including where DuckDB is the wrong choice. Measure organic entrances and assisted signups per page, and check whether the pages get cited in AI assistant answers, since a growing share of these questions now get asked there.

**Confidence.** The question grouping is pattern-matched and manually filtered, not the item-by-item read used for topic tagging. Treat the counts as approximate.

---

## What I'm not pitching, and why

AI agents and MCP is the single biggest mover in the data. It went from zero items in 2022 to 8.7% and 165 items in the last twelve months, and it is tied as the largest build category at 47 projects. On the data alone it is the obvious pitch.

I am not pitching it because MotherDuck has run seven agent-themed online events in the last three months, five of them in August alone: Flights, agent-led onboarding, agent evaluation with Braintrust, Guides, a live stack build with dltHub and Lightdash, and a semantic layer debate. That is roughly one every two weeks, and the cadence is accelerating rather than steady.

DuckLake is the second-biggest mover, from 1.6% to 6.1%, and was covered on 3 September. Data pipelines and ETL is the other 47-project build category, tied with agents and ahead of browser and WASM at 41, and has been covered repeatedly with Spark and Iceberg, Postgres CDC, and robust pipelines with AI.

All three are correctly identified by the data and already served. The gap is not in what MotherDuck is talking about. It is in what has been left alone while agents took the calendar.

---

## What changed since 2022

| Topic | 2022 (n) | 2022 % | Recent (n) | Recent % | Change |
|---|---:|---:|---:|---:|---:|
| Python and notebook workflows | 41 | 10.9% | 74 | 3.9% | −7.0pp |
| General or other | 173 | 45.9% | 790 | 41.7% | −4.2pp |
| Local vs cloud execution | 63 | 16.7% | 241 | 12.7% | −4.0pp |
| Postgres integration | 25 | 6.6% | 82 | 4.3% | −2.3pp |
| Cost and pricing vs other warehouses | 2 | 0.5% | 35 | 1.8% | +1.3pp |
| Performance and benchmarks | 65 | 17.2% | 352 | 18.6% | +1.3pp |
| Customer-facing and embedded analytics | 2 | 0.5% | 42 | 2.2% | +1.7pp |
| DuckLake and lakehouse formats | 6 | 1.6% | 115 | 6.1% | +4.5pp |
| AI agents and MCP | 0 | 0.0% | 165 | 8.7% | +8.7pp |

Two notes on reading this table. Share and raw count move in opposite directions for several topics. Python fell 7 points in share while rising from 41 items to 74, and local vs cloud fell 4 points while rising from 63 to 241. Both conversations grew in absolute terms while others grew faster. I am reporting both numbers rather than picking the more flattering one, and I have not tried to explain which of the two effects dominates, because this data cannot separate them.

The two corpora are also different sizes and cover different spans, so shares are comparable and raw counts are not.

---

## Limits

**Precision.** I hand-labelled a stratified 50-item sample for whether DuckDB or MotherDuck was actually the subject rather than a passing mention. Overall precision was 80.0%, 90.9% on stories (n=11) and 76.9% on comments (n=39). The story and comment figures sit on small samples and I would not lean on the gap between them.

**The labelling rule.** An item counted if the person was engaging with what DuckDB or MotherDuck does: asking about it, arguing about it, using it, or explaining it. It did not count if DuckDB appeared only in a list of tools or as praise with no substance. Hiring threads were a consistent source of false positives.

**Nine of the 50 sampled items** were title-and-URL-only stories with no body text. For two of those, the only evidence was in the URL, one pointing at MotherDuck's own blog and one at a react-native-duckdb repository. I mislabelled both before adding a URL column. Any pipeline reading only title and text would have got those wrong.

**Engagement scores are stories-only.** The `points` field is null for all comments in the HN data model, so any ranking by score excludes 78% of the recent corpus.

**A news event in late August** produced a one-time spike in volume, accounting for 62 items. Recent-month totals are inflated relative to the baseline and August topic shares should be read with that in mind.

**The 2022 corpus is a partial year.** MotherDuck's sample table runs from 1 January to 16 November 2022, so it covers ten and a half months against twelve for the recent window.

**The corpus is Hacker News**, which is where developers in general discuss DuckDB. It is not MotherDuck's user base, its signups, or its churned accounts. People who argue about benchmarks in public are not necessarily people who give a vendor their email, and I have no data on the second group. Inside the company I would run this against product usage, signup source and activation data, and treat public discussion as one input rather than the measure.

---

## Method

**The data.** Two corpora in one table. The first is MotherDuck's own `sample_data.hn.hacker_news`, filtered to rows mentioning DuckDB or MotherDuck. That table covers 1 January to 16 November 2022 only, and yielded 377 items, 326 comments and 51 stories. The second is the last twelve months, pulled from the Algolia Hacker News API, 1,896 items, 1,487 comments and 409 stories. Both were normalised to the same columns and tagged with an `era` field so the two periods could be compared in a single query. 2,273 rows in total, all of it in MotherDuck.

**Collecting the recent corpus.** Three things went wrong before the data was usable. Algolia's tag syntax needs parentheses around an OR list, and a bare comma is read as AND, which returned zero results without any error. The API also caps any single query at roughly 1,000 retrievable results while still reporting a higher total, so a twelve-month request would have silently dropped the oldest items. I chunked the fetch by month to stay under the cap, with a recursive split if any single month exceeded it. Finally, Algolia's typo tolerance was matching duck.ai and DuckDuckGo, so I turned it off and confirmed the remaining matches contained the literal term.

**Relevance check.** Keyword matching finds every mention, including the ones where DuckDB is just a name in a list, so I measured how often the match was real. I hand-labelled a stratified 50-item sample, proportional to the story and comment split of the full corpus. My rule: an item counts if the person is engaging with what DuckDB or MotherDuck does, whether asking about it, arguing about it, using it or explaining it. It does not count if DuckDB appears only in a list of tools or as praise with no substance behind it. Hiring threads were the most consistent source of false positives. Precision came out at 80.0% overall, 90.9% on stories and 76.9% on comments, though both of those sit on small samples.

**The URL blind spot.** Nine of the 50 sampled items were title-and-URL-only stories with no body text at all. For two of them, the only evidence that the item was about DuckDB sat in the URL: one pointed at MotherDuck's own blog, the other at a react-native-duckdb repository. I labelled both incorrectly before adding a URL column to the review file. Any pipeline reading only title and text would have got them wrong, and I would not have caught it without reading the sample by hand.

**Topic tagging.** My first attempt used keyword rules, and it pushed 50.8% of the corpus into "general or other." Reading the failures showed why. A comment about concurrency limits and ingestion rates is plainly a performance discussion to a human, but the rules only fired on literal words like "benchmark" or "faster." I dropped that approach and tagged by reading each item instead, across 23 batches of roughly 100. The final "general or other" rate was 42.4%. Still high, but now a real finding rather than a classifier blind spot: a large share of organic Hacker News chatter about DuckDB genuinely does not map to any specific theme.

---

## Reproducing this

https://github.com/dhishasuresh-commits/motherduck-webinar-analysis

Built with Claude Code. The analysis runs in MotherDuck against a table combining both corpora.
