#!/usr/bin/env python3
"""Regression-test semantic question routing against PROJECT_KNOWLEDGE_MAP.json."""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STOP = {
    "der","die","das","den","dem","des","ein","eine","einer","einen","einem",
    "ist","sind","war","wurde","wie","was","wo","warum","welche","welcher","welches",
    "und","oder","mit","auf","in","im","am","an","zu","von","fuer","für","ich","jetzt",
    "the","a","an","is","are","what","where","why","how","and","or","to","of","with"
}


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower().replace("-", " ").replace("_", " ")
    return " ".join(re.findall(r"[a-z0-9.]+", text))


def tokens(text: str) -> set[str]:
    return {t for t in norm(text).split() if t not in STOP and len(t) > 1}


def score(query: str, topic: dict) -> tuple[int, int, str]:
    nq = norm(query)
    qtokens = tokens(query)
    best = (0, 0, "")
    phrases = [topic.get("id", ""), topic.get("title", ""), *topic.get("aliases", [])]
    for phrase in phrases:
        np = norm(str(phrase))
        if not np:
            continue
        ptokens = tokens(np)
        exact_phrase = np in nq
        overlap = len(qtokens & ptokens)
        # Exact semantic phrases dominate. Otherwise reward token coverage and specificity.
        primary = (1000 if exact_phrase else 0) + overlap * 100
        secondary = len(ptokens) * 10 + len(np)
        candidate = (primary, secondary, np)
        if candidate > best:
            best = candidate
    return best


def route(query: str, topics: list[dict]) -> tuple[dict, tuple[int, int, str]]:
    ranked = sorted(((score(query, t), t) for t in topics), key=lambda x: (x[0], x[1].get("id", "")), reverse=True)
    best_score, best_topic = ranked[0]
    if best_score[0] <= 0:
        raise RuntimeError(f"no semantic route for query: {query}")
    return best_topic, best_score


def main() -> int:
    km = json.loads((ROOT / "Current/PROJECT_KNOWLEDGE_MAP.json").read_text(encoding="utf-8"))
    cases = json.loads((ROOT / "RepositoryTools/answerability_cases.json").read_text(encoding="utf-8"))
    topics = km.get("topics", [])
    topic_by_id = {t["id"]: t for t in topics}
    errors: list[str] = []

    for case in cases.get("cases", []):
        expected_id = case["expected_topic"]
        expected_canonical = case["expected_canonical"]
        if expected_id not in topic_by_id:
            errors.append(f"{case['id']}: expected topic missing: {expected_id}")
            continue
        if topic_by_id[expected_id].get("canonical") != expected_canonical:
            errors.append(
                f"{case['id']}: expected canonical drift: map={topic_by_id[expected_id].get('canonical')} case={expected_canonical}"
            )
            continue
        if not (ROOT / expected_canonical).exists():
            errors.append(f"{case['id']}: expected canonical path missing: {expected_canonical}")
            continue

        try:
            routed, routed_score = route(case["query"], topics)
        except Exception as exc:
            errors.append(f"{case['id']}: router error: {exc}")
            continue
        if routed.get("id") != expected_id:
            errors.append(
                f"{case['id']}: routed to {routed.get('id')} instead of {expected_id}; "
                f"score={routed_score}; query={case['query']!r}"
            )
        else:
            print(f"PASS {case['id']}: {expected_id} -> {expected_canonical}")

    print(f"Answerability routing cases={len(cases.get('cases', []))} errors={len(errors)}")
    for error in errors:
        print("ERROR:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
