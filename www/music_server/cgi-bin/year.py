#!/usr/bin/env python3
import os
import sys
import json
import urllib.parse

HITS = {
    2000: {
        "song": "Breathe",
        "artist": "Faith Hill",
        "note": "A country-pop crossover that anchored the top of the Billboard Year-End chart as the 90s bled into the 2000s — lush, warm, and unshakably polished.",
        "tags": ["Country-Pop", "Billboard YE #1", "Crossover"],
    },
    2001: {
        "song": "Hanging by a Moment",
        "artist": "Lifehouse",
        "note": "Post-grunge with a melodic soft-rock heart. It never hit #1 weekly, but it stayed on the Hot 100 long enough to take the year-end crown.",
        "tags": ["Post-Grunge", "Soft Rock", "Billboard YE #1"],
    },
    2002: {
        "song": "How You Remind Me",
        "artist": "Nickelback",
        "note": "The year's radio backbone. Love it or roast it, it defined early-00s rock radio in North America.",
        "tags": ["Alt-Rock", "Radio", "Billboard YE #1"],
    },
    2003: {
        "song": "In Da Club",
        "artist": "50 Cent",
        "note": "Dr. Dre production, G-Unit bravado and an intro that every gym, club and ringtone memorised by heart.",
        "tags": ["Hip-Hop", "West Coast", "Billboard YE #1"],
    },
    2004: {
        "song": "Yeah!",
        "artist": "Usher ft. Lil Jon & Ludacris",
        "note": "Crunk&B at its zenith. Lil Jon's synth stabs did half the work, Usher the rest. Peaked 12 weeks at #1.",
        "tags": ["Crunk", "R&B", "Billboard YE #1"],
    },
    2005: {
        "song": "We Belong Together",
        "artist": "Mariah Carey",
        "note": "The comeback — 14 weeks at #1 and a reminder that melisma plus restraint beats everyone else's octaves.",
        "tags": ["R&B", "Ballad", "Billboard YE #1"],
    },
    2006: {
        "song": "Bad Day",
        "artist": "Daniel Powter",
        "note": "Anointed by American Idol's elimination reel, and later the whole world. Piano-pop comfort food.",
        "tags": ["Piano-Pop", "Billboard YE #1"],
    },
    2007: {
        "song": "Irreplaceable",
        "artist": "Beyoncé",
        "note": "The 'to the left, to the left' ultimatum. 10 weeks at #1 and the blueprint for every breakup song that followed.",
        "tags": ["R&B", "Pop", "Billboard YE #1"],
    },
    2008: {
        "song": "Low",
        "artist": "Flo Rida ft. T-Pain",
        "note": "T-Pain's auto-tune hook was inescapable. Apple Bottom jeans entered the cultural dictionary.",
        "tags": ["Hip-Hop", "Club", "Billboard YE #1"],
    },
    2009: {
        "song": "Boom Boom Pow",
        "artist": "The Black Eyed Peas",
        "note": "The year pop went full electro. will.i.am's maximalist beat sat at #1 for 12 weeks and opened the door for the EDM era.",
        "tags": ["Electro-Pop", "Dance", "Billboard YE #1"],
    },
    2010: {
        "song": "Tik Tok",
        "artist": "Kesha",
        "note": "Party-starter in a glitter jumpsuit. Dr. Luke / Benny Blanco production that defined 2010 radio.",
        "tags": ["Electro-Pop", "Party", "Billboard YE #1"],
    },
    2011: {
        "song": "Rolling in the Deep",
        "artist": "Adele",
        "note": "'21' was the moment soul crashed back into the mainstream. A voice, a kick drum, and zero apology.",
        "tags": ["Soul", "Pop", "Billboard YE #1"],
    },
    2012: {
        "song": "Somebody That I Used to Know",
        "artist": "Gotye ft. Kimbra",
        "note": "An indie Australian record that went planetary. Xylophone, heartbreak and the year's definitive duet.",
        "tags": ["Indie-Pop", "Alt", "Billboard YE #1"],
    },
    2013: {
        "song": "Thrift Shop",
        "artist": "Macklemore & Ryan Lewis ft. Wanz",
        "note": "A self-released indie hip-hop single that dethroned major labels — 6 weeks at #1, and a moment for hook-writer Wanz.",
        "tags": ["Hip-Hop", "Indie", "Billboard YE #1"],
    },
    2014: {
        "song": "Happy",
        "artist": "Pharrell Williams",
        "note": "From Despicable Me 2 to the Oscars to every dentist waiting room in the world. Impossible not to hear it in 2014.",
        "tags": ["Pop-Soul", "Feel-Good", "Billboard YE #1"],
    },
    2015: {
        "song": "Uptown Funk",
        "artist": "Mark Ronson ft. Bruno Mars",
        "note": "14 weeks at #1. Ronson engineered a disco-funk time machine and Bruno climbed in and refused to leave.",
        "tags": ["Funk", "Disco-Pop", "Billboard YE #1"],
    },
    2016: {
        "song": "Love Yourself",
        "artist": "Justin Bieber",
        "note": "Co-written by Ed Sheeran. Acoustic, polite, and quietly devastating — Bieber's redemption lap.",
        "tags": ["Acoustic-Pop", "Billboard YE #1"],
    },
    2017: {
        "song": "Shape of You",
        "artist": "Ed Sheeran",
        "note": "Afro-dancehall rhythm laced with pop songwriter instincts. 12 weeks at #1 and the year's streaming monster.",
        "tags": ["Pop", "Dancehall", "Billboard YE #1"],
    },
    2018: {
        "song": "God's Plan",
        "artist": "Drake",
        "note": "From 'Scary Hours' into 'Scorpion'. 11 weeks at #1, a music video that just gave money away, and hooks on loop for months.",
        "tags": ["Hip-Hop", "Melodic Rap", "Billboard YE #1"],
    },
    2019: {
        "song": "Old Town Road",
        "artist": "Lil Nas X ft. Billy Ray Cyrus",
        "note": "Country-trap that broke the Hot 100 record with 19 weeks at #1. A meme, a movement, a genre debate.",
        "tags": ["Country-Trap", "Viral", "Billboard YE #1"],
    },
    2020: {
        "song": "Blinding Lights",
        "artist": "The Weeknd",
        "note": "Synthwave dressed in retro neon. Later crowned the longest-charting Hot 100 song ever. 2020's sonic identity.",
        "tags": ["Synthwave", "Pop", "Billboard YE #1"],
    },
    2021: {
        "song": "Levitating",
        "artist": "Dua Lipa ft. DaBaby",
        "note": "Future Nostalgia's disco-pop made 2021 feel like a dance floor you weren't allowed to visit. Billboard YE #1.",
        "tags": ["Disco-Pop", "Dance", "Billboard YE #1"],
    },
    2022: {
        "song": "As It Was",
        "artist": "Harry Styles",
        "note": "Synth-pop melancholy wrapped in 80s gauze. 15 weeks at #1 and the defining sound of post-pandemic pop.",
        "tags": ["Synth-Pop", "Indie-Pop", "Billboard YE #1"],
    },
    2023: {
        "song": "Flowers",
        "artist": "Miley Cyrus",
        "note": "A self-love anthem engineered like a disco-rock hymn. 8 weeks at #1 and a Grammy for Record of the Year.",
        "tags": ["Pop-Rock", "Disco", "Billboard YE #1"],
    },
    2024: {
        "song": "A Bar Song (Tipsy)",
        "artist": "Shaboozey",
        "note": "Country-pop that sampled J-Kwon's 'Tipsy' — tied the record for longest-running Hot 100 #1 at 19 weeks.",
        "tags": ["Country-Pop", "Crossover", "Billboard YE #1"],
    },
    2025: {
        "song": "Die With a Smile",
        "artist": "Lady Gaga & Bruno Mars",
        "note": "A slow-burn duet that dominated the Hot 100 into 2025. Two pop powerhouses trading verses like a 70s rock ballad.",
        "tags": ["Pop", "Ballad", "Duet"],
    },
}


def parse_query():
    qs = os.environ.get("QUERY_STRING", "")
    params = urllib.parse.parse_qs(qs)
    try:
        return int(params.get("y", ["0"])[0])
    except ValueError:
        return 0


def send_json(payload, status=200):
    sys.stdout.write("Status: {} OK\r\n".format(status))
    sys.stdout.write("Content-Type: application/json; charset=utf-8\r\n\r\n")
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    sys.stdout.flush()


def main():
    year = parse_query()
    if year not in HITS:
        send_json({"error": "Unknown year", "year": year}, status=404)
        return
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
