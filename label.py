#!/usr/bin/env python3
import csv

CSV_PATH = "data/relevance_check.csv"


def load_rows():
    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    return fieldnames, rows


def save_rows(fieldnames, rows):
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def rate(subset):
    labeled = [r for r in subset if r["relevant"] in ("1", "0")]
    if not labeled:
        return None
    pos = sum(1 for r in labeled if r["relevant"] == "1")
    return pos, len(labeled), pos / len(labeled)


def print_stats(rows):
    print("\n=== Results ===")
    for label, subset in [
        ("Overall", rows),
        ("Story", [r for r in rows if r["type"] == "story"]),
        ("Comment", [r for r in rows if r["type"] == "comment"]),
    ]:
        result = rate(subset)
        if result:
            pos, n, frac = result
            print(f"{label:8} precision: {pos}/{n} = {frac:.1%}")
        else:
            print(f"{label:8} precision: no labeled rows")

    skipped = sum(1 for r in rows if r["relevant"] == "s")
    if skipped:
        print(f"(Skipped: {skipped})")


def main():
    fieldnames, rows = load_rows()
    total = len(rows)
    remaining = [i for i, r in enumerate(rows) if not r.get("relevant")]

    if not remaining:
        print(f"All {total} rows already labeled.")
        print_stats(rows)
        return

    print(f"{len(remaining)} of {total} rows left to label.")
    print("Type 1 (relevant), 0 (not relevant), or s (skip). Ctrl+C anytime to quit and resume later.\n")

    try:
        for idx in remaining:
            row = rows[idx]
            print(f"--- Row {idx + 1}/{total} ---")
            print(f"Date:  {row['date']}")
            print(f"Type:  {row['type']}")
            print(f"Title: {row['title']}")
            print(f"Context: {row['keyword_context']}")
            while True:
                answer = input("Relevant? [1/0/s]: ").strip().lower()
                if answer in ("1", "0", "s"):
                    break
                print("Please type 1, 0, or s.")
            row["relevant"] = answer
            save_rows(fieldnames, rows)
            print()
    except (KeyboardInterrupt, EOFError):
        print("\n\nSaved progress. Resume anytime by rerunning label.py.")
        return

    print("All rows labeled.\n")
    print_stats(rows)


if __name__ == "__main__":
    main()
