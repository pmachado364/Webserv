#!/usr/bin/env python3

import sys, os, urllib.parse, json, random

content_length = int(os.environ.get('CONTENT_LENGTH', 0))
body = sys.stdin.buffer.read(content_length).decode('utf-8', errors='replace') if content_length else ''
params = urllib.parse.parse_qs(body)
name = params.get('name', ['friend'])[0][:60].strip() or 'friend'

OPENERS = [
    "you know what?",
    "not to be dramatic but",
    "science has confirmed that",
    "the data is clear:",
    "for real though,",
    "objectively speaking,",
]

COMPLIMENTS = [
    "your brain operates at a frequency most people can only dream of.",
    "you have the rare ability to make every room feel warmer.",
    "your laugh is the kind that makes strangers smile.",
    "you tackle hard problems like they owe you money.",
    "you radiate a very specific energy that makes things better.",
    "your taste is impeccable and it shows in everything you do.",
    "you're the kind of person people tell stories about with a smile.",
    "you make complexity look effortless.",
    "your curiosity is genuinely infectious.",
    "you leave things better than you found them — every single time.",
    "the way you carry yourself is something people notice immediately.",
    "you're sharper than you give yourself credit for.",
    "honestly? you're a lot to live up to.",
    "the world is measurably better with you in it.",
    "you have a sixth sense for what actually matters.",
]

opener = random.choice(OPENERS)
compliment = random.choice(COMPLIMENTS)

print("Content-Type: application/json")
print()
print(json.dumps({
    "greeting": f"{name},",
    "compliment": f"{opener} {compliment}"
}), flush=True)
