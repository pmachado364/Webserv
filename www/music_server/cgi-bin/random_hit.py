#!/usr/bin/env python3
import sys
import json
import random

HITS = {
    2000: {"song": "Breathe", "artist": "Faith Hill",
           "note": "Country-pop crossover that anchored the top of the Billboard Year-End chart as the 90s bled into the 2000s.",
           "tags": ["Country-Pop", "Billboard YE #1"]},
    2001: {"song": "Hanging by a Moment", "artist": "Lifehouse",
           "note": "Never hit #1 weekly but stayed on the Hot 100 long enough to take the year-end crown.",
           "tags": ["Post-Grunge", "Soft Rock"]},
    2002: {"song": "How You Remind Me", "artist": "Nickelback",
           "note": "The year's radio backbone — defined early-00s rock radio in North America.",
           "tags": ["Alt-Rock", "Radio"]},
    2003: {"song": "In Da Club", "artist": "50 Cent",
           "note": "Dr. Dre production, G-Unit bravado and an intro every gym memorised by heart.",
           "tags": ["Hip-Hop", "West Coast"]},
    2004: {"song": "Yeah!", "artist": "Usher ft. Lil Jon & Ludacris",
           "note": "Crunk&B at its zenith. 12 weeks at #1.",
           "tags": ["Crunk", "R&B"]},
    2005: {"song": "We Belong Together", "artist": "Mariah Carey",
           "note": "14 weeks at #1 — melisma plus restraint.",
           "tags": ["R&B", "Ballad"]},
    2006: {"song": "Bad Day", "artist": "Daniel Powter",
           "note": "Anointed by American Idol's elimination reel, then the whole world.",
           "tags": ["Piano-Pop"]},
    2007: {"song": "Irreplaceable", "artist": "Beyoncé",
           "note": "The 'to the left, to the left' ultimatum — 10 weeks at #1.",
           "tags": ["R&B", "Pop"]},
    2008: {"song": "Low", "artist": "Flo Rida ft. T-Pain",
           "note": "T-Pain's auto-tune hook was inescapable. Apple Bottom jeans entered the dictionary.",
           "tags": ["Hip-Hop", "Club"]},
    2009: {"song": "Boom Boom Pow", "artist": "The Black Eyed Peas",
           "note": "will.i.am's maximalist beat opened the door for the EDM era.",
           "tags": ["Electro-Pop", "Dance"]},
    2010: {"song": "Tik Tok", "artist": "Kesha",
           "note": "Party-starter in a glitter jumpsuit. Dr. Luke / Benny Blanco production.",
           "tags": ["Electro-Pop", "Party"]},
    2011: {"song": "Rolling in the Deep", "artist": "Adele",
           "note": "Soul crashed back into the mainstream. A voice, a kick drum, zero apology.",
           "tags": ["Soul", "Pop"]},
    2012: {"song": "Somebody That I Used to Know", "artist": "Gotye ft. Kimbra",
           "note": "Xylophone, heartbreak and the year's definitive duet.",
           "tags": ["Indie-Pop", "Alt"]},
    2013: {"song": "Thrift Shop", "artist": "Macklemore & Ryan Lewis ft. Wanz",
           "note": "A self-released indie hip-hop single that dethroned major labels.",
           "tags": ["Hip-Hop", "Indie"]},
    2014: {"song": "Happy", "artist": "Pharrell Williams",
           "note": "From Despicable Me 2 to the Oscars to every dentist in the world.",
           "tags": ["Pop-Soul", "Feel-Good"]},
    2015: {"song": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars",
           "note": "14 weeks at #1. A disco-funk time machine.",
           "tags": ["Funk", "Disco-Pop"]},
    2016: {"song": "Love Yourself", "artist": "Justin Bieber",
           "note": "Co-written by Ed Sheeran. Acoustic and quietly devastating.",
           "tags": ["Acoustic-Pop"]},
    2017: {"song": "Shape of You", "artist": "Ed Sheeran",
           "note": "Afro-dancehall rhythm + pop instincts. The year's streaming monster.",
           "tags": ["Pop", "Dancehall"]},
    2018: {"song": "God's Plan", "artist": "Drake",
           "note": "11 weeks at #1. The music video that just gave money away.",
           "tags": ["Hip-Hop", "Melodic Rap"]},
    2019: {"song": "Old Town Road", "artist": "Lil Nas X ft. Billy Ray Cyrus",
           "note": "Country-trap that broke records with 19 weeks at #1.",
           "tags": ["Country-Trap", "Viral"]},
    2020: {"song": "Blinding Lights", "artist": "The Weeknd",
           "note": "Synthwave in retro neon. Longest-charting Hot 100 song ever.",
           "tags": ["Synthwave", "Pop"]},
    2021: {"song": "Levitating", "artist": "Dua Lipa ft. DaBaby",
           "note": "Future Nostalgia's disco-pop. Billboard YE #1.",
           "tags": ["Disco-Pop", "Dance"]},
    2022: {"song": "As It Was", "artist": "Harry Styles",
           "note": "Synth-pop melancholy in 80s gauze. 15 weeks at #1.",
           "tags": ["Synth-Pop", "Indie-Pop"]},
    2023: {"song": "Flowers", "artist": "Miley Cyrus",
           "note": "Self-love anthem engineered as a disco-rock hymn. Grammy Record of the Year.",
           "tags": ["Pop-Rock", "Disco"]},
    2024: {"song": "A Bar Song (Tipsy)", "artist": "Shaboozey",
           "note": "Country-pop that sampled J-Kwon's 'Tipsy'. Tied the record for longest Hot 100 #1 at 19 weeks.",
           "tags": ["Country-Pop", "Crossover"]},
    2025: {"song": "Die With a Smile", "artist": "Lady Gaga & Bruno Mars",
           "note": "A slow-burn duet that dominated the Hot 100 into 2025.",
           "tags": ["Pop", "Ballad", "Duet"]},
}


def send_json(payload):
    sys.stdout.write("Content-Type: application/json; charset=utf-8\r\n\r\n")
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    sys.stdout.flush()


def main():
    year = random.choice(list(HITS.keys()))
    entry = HITS[year]
    send_json({
        "year": year,
        "song": entry["song"],
        "artist": entry["artist"],
        "note": entry["note"],
        "tags": entry["tags"],
    })


if __name__ == "__main__":
    main()
