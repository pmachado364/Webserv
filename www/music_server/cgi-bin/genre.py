#!/usr/bin/env python3
import os
import sys
import json
import urllib.parse

GENRES = {
    "pop": {
        "name": "Pop",
        "tagline": "Five songs that held the mainstream by the throat",
        "tracks": [
            {"song": "Toxic", "artist": "Britney Spears", "year": 2004},
            {"song": "Poker Face", "artist": "Lady Gaga", "year": 2009},
            {"song": "Rolling in the Deep", "artist": "Adele", "year": 2011},
            {"song": "Shape of You", "artist": "Ed Sheeran", "year": 2017},
            {"song": "Blinding Lights", "artist": "The Weeknd", "year": 2020},
        ],
    },
    "hiphop": {
        "name": "Hip-Hop",
        "tagline": "Five cuts that re-drew the map of the charts",
        "tracks": [
            {"song": "In Da Club", "artist": "50 Cent", "year": 2003},
            {"song": "Lose Yourself", "artist": "Eminem", "year": 2002},
            {"song": "Empire State of Mind", "artist": "Jay-Z ft. Alicia Keys", "year": 2009},
            {"song": "HUMBLE.", "artist": "Kendrick Lamar", "year": 2017},
            {"song": "Sicko Mode", "artist": "Travis Scott", "year": 2018},
        ],
    },
    "rock": {
        "name": "Rock",
        "tagline": "Loud, honest, and refusing to be a nostalgia act",
        "tracks": [
            {"song": "Seven Nation Army", "artist": "The White Stripes", "year": 2003},
            {"song": "Mr. Brightside", "artist": "The Killers", "year": 2004},
            {"song": "American Idiot", "artist": "Green Day", "year": 2004},
            {"song": "Viva la Vida", "artist": "Coldplay", "year": 2008},
            {"song": "Radioactive", "artist": "Imagine Dragons", "year": 2012},
        ],
    },
    "rnb": {
        "name": "R&B",
        "tagline": "Velvet vocals, slick production, and all the feelings",
        "tracks": [
            {"song": "Crazy in Love", "artist": "Beyoncé ft. Jay-Z", "year": 2003},
            {"song": "We Belong Together", "artist": "Mariah Carey", "year": 2005},
            {"song": "Umbrella", "artist": "Rihanna ft. Jay-Z", "year": 2007},
            {"song": "Thinkin Bout You", "artist": "Frank Ocean", "year": 2012},
            {"song": "Kill Bill", "artist": "SZA", "year": 2022},
        ],
    },
    "edm": {
        "name": "EDM",
        "tagline": "The five drops that moved dance floors from warehouses to stadiums",
        "tracks": [
            {"song": "Sandstorm", "artist": "Darude", "year": 2000},
            {"song": "One More Time", "artist": "Daft Punk", "year": 2000},
            {"song": "Levels", "artist": "Avicii", "year": 2011},
            {"song": "Titanium", "artist": "David Guetta ft. Sia", "year": 2011},
            {"song": "Don't You Worry Child", "artist": "Swedish House Mafia", "year": 2012},
        ],
    },
    "country": {
        "name": "Country",
        "tagline": "Boot-stomp, heartbreak, and the slow-burn crossover",
        "tracks": [
            {"song": "Before He Cheats", "artist": "Carrie Underwood", "year": 2006},
            {"song": "Need You Now", "artist": "Lady A", "year": 2009},
            {"song": "Cruise", "artist": "Florida Georgia Line", "year": 2012},
            {"song": "Meant to Be", "artist": "Bebe Rexha & Florida Georgia Line", "year": 2017},
            {"song": "A Bar Song (Tipsy)", "artist": "Shaboozey", "year": 2024},
        ],
    },
    "latin": {
        "name": "Latin",
        "tagline": "Reggaeton, bolero modernizado, and global takeover",
        "tracks": [
            {"song": "Gasolina", "artist": "Daddy Yankee", "year": 2004},
            {"song": "Despacito", "artist": "Luis Fonsi & Daddy Yankee ft. Bieber", "year": 2017},
            {"song": "Mi Gente", "artist": "J Balvin & Willy William", "year": 2017},
            {"song": "Dákiti", "artist": "Bad Bunny & Jhay Cortez", "year": 2020},
            {"song": "Bzrp Music Sessions #53", "artist": "Shakira & Bizarrap", "year": 2023},
        ],
    },
    "indie": {
        "name": "Indie",
        "tagline": "Left of the dial, loud in the heart",
        "tracks": [
            {"song": "Float On", "artist": "Modest Mouse", "year": 2004},
            {"song": "Young Folks", "artist": "Peter Bjorn and John", "year": 2006},
            {"song": "Skinny Love", "artist": "Bon Iver", "year": 2008},
            {"song": "Pumped Up Kicks", "artist": "Foster the People", "year": 2011},
            {"song": "Vampire", "artist": "Olivia Rodrigo", "year": 2023},
        ],
    },
}


def parse_query():
    qs = os.environ.get("QUERY_STRING", "")
    params = urllib.parse.parse_qs(qs)
    return (params.get("g", [""])[0] or "").lower()


def send_json(payload, status=200):
    sys.stdout.write("Status: {} OK\r\n".format(status))
    sys.stdout.write("Content-Type: application/json; charset=utf-8\r\n\r\n")
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    sys.stdout.flush()


def main():
    g = parse_query()
    if g not in GENRES:
        send_json({"error": "Unknown genre", "genre": g}, status=404)
        return
    send_json(GENRES[g])


if __name__ == "__main__":
    main()
