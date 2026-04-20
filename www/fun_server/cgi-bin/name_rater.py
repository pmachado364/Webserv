#!/usr/bin/env python3

import sys, os, urllib.parse, json, random

content_length = int(os.environ.get('CONTENT_LENGTH', 0))
body = sys.stdin.buffer.read(content_length).decode('utf-8', errors='replace') if content_length else ''
params = urllib.parse.parse_qs(body)
name = params.get('name', ['Anonymous'])[0][:60].strip() or 'Anonymous'

TIERS = [
    (90, "S-TIER NAME",  "Statistically speaking, this name carries enormous cultural gravity. People remember it, trust it, and secretly wish they had it."),
    (80, "A-TIER NAME",  "A highly reliable name with strong phonetic energy. Performs well under pressure. Aged like fine wine."),
    (70, "B-TIER NAME",  "Solid, dependable, globally recognisable. May not turn heads, but always delivers. The backbone of civilisation."),
    (60, "C-TIER NAME",  "Respectable, if unremarkable. Carries quiet dignity. The kind of name that gets the job done without fanfare."),
    (50, "D-TIER NAME",  "Functional. Present. Technically a name. Scientists are still studying its long-term effects on social dynamics."),
    (0,  "UNCLASSIFIED", "Our instruments are struggling to categorise this one. That's either very concerning or absolutely legendary."),
]

# deterministic-ish score from the name's characters
seed_val = sum(ord(c) * (i + 1) for i, c in enumerate(name.lower()[:8]))
random.seed(seed_val)
score = random.randint(42, 99)

tier_label = TIERS[-1][1]
analysis   = TIERS[-1][2]
for threshold, label, text in TIERS:
    if score >= threshold:
        tier_label = label
        analysis   = text
        break

print("Content-Type: application/json")
print()
print(json.dumps({
    "name":     name,
    "score":    score,
    "tier":     tier_label,
    "analysis": analysis
}), flush=True)
