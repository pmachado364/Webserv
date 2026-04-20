#!/usr/bin/env python3

import sys, os, urllib.parse, json, random

content_length = int(os.environ.get('CONTENT_LENGTH', 0))
body = sys.stdin.buffer.read(content_length).decode('utf-8', errors='replace') if content_length else ''
params = urllib.parse.parse_qs(body)
mood = params.get('mood', ['neutral'])[0][:120].strip().lower() or 'neutral'

VIBES = [
    {
        "emoji": "⚡",
        "vibe": "HIGH VOLTAGE",
        "verdict": "Your energy could power a small city right now. Channel it wisely — the world isn't ready."
    },
    {
        "emoji": "🌊",
        "vibe": "DEEP CURRENT",
        "verdict": "Calm on the surface, forces in motion underneath. Things are moving even when it doesn't feel like it."
    },
    {
        "emoji": "🌙",
        "vibe": "LUNAR DRIFT",
        "verdict": "You're in a reflective, introspective mode. This is actually a superpower — let it run."
    },
    {
        "emoji": "🔥",
        "vibe": "MAIN CHARACTER",
        "verdict": "The plot is accelerating and you are clearly the protagonist. Lean into it."
    },
    {
        "emoji": "🌿",
        "vibe": "GROUNDED",
        "verdict": "Steady. Rooted. Unbothered. This is the rarest and most underrated energy there is."
    },
    {
        "emoji": "🎯",
        "vibe": "LOCKED IN",
        "verdict": "Whatever you're aiming at, you're closer than you think. Don't lift your eyes off the target."
    },
    {
        "emoji": "🌀",
        "vibe": "TRANSITIONAL",
        "verdict": "Something is shifting. It's disorienting — that's normal. The signal-to-noise ratio will improve."
    },
    {
        "emoji": "✨",
        "vibe": "LUMINOUS",
        "verdict": "You are emitting at a frequency people can't quite explain but definitely feel. Keep it up."
    },
    {
        "emoji": "🧊",
        "vibe": "ICE COLD",
        "verdict": "Unaffected. Unshaken. Operating purely on logic and precision. Honestly iconic."
    },
    {
        "emoji": "🎲",
        "vibe": "CHAOTIC NEUTRAL",
        "verdict": "Unpredictable and impossible to read. Somehow everything works out anyway. Classic."
    },
]

# bias the pick using the length of the mood string for fun determinism
random.seed(len(mood) * 7 + sum(ord(c) for c in mood[:10]))
result = random.choice(VIBES)

print("Content-Type: application/json")
print()
print(json.dumps(result), flush=True)
