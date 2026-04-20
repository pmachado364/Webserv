#!/usr/bin/env python3

import sys, os, urllib.parse, json, random

content_length = int(os.environ.get('CONTENT_LENGTH', 0))
body = sys.stdin.buffer.read(content_length).decode('utf-8', errors='replace') if content_length else ''
params = urllib.parse.parse_qs(body)
question = params.get('question', ['What lies ahead?'])[0][:120].strip() or 'What lies ahead?'

FORTUNES = [
    "The answer you seek hides behind the question you haven't asked yet.",
    "Three paths open before you. The shortest one is not the easiest.",
    "What feels like an ending is simply the universe clearing space for something better.",
    "The stars are not indifferent — they are merely patient.",
    "You already know the answer. You came here hoping to be told otherwise.",
    "Trust the instinct you keep second-guessing.",
    "The obstacle and the path are the same thing.",
    "A door is about to open that you forgot you knocked on.",
    "Not all questions deserve answers. This one, however, deserves action.",
    "Your next move is obvious to everyone except you.",
    "The timing feels wrong because you are measuring with the wrong clock.",
    "Someone from your past holds a key you forgot you gave them.",
    "Look again. The thing you almost dismissed will matter most.",
    "The universe does not do coincidences. Pay attention to what keeps repeating.",
    "It is closer than it appears. Proceed accordingly.",
    "What you fear is a shadow cast by something that no longer stands.",
    "The answer is yes — but not today.",
    "Fortune favours the one who prepares and then lets go.",
]

print("Content-Type: application/json")
print()
print(json.dumps({
    "question": question,
    "fortune": random.choice(FORTUNES)
}), flush=True)
