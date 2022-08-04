# ------------------------------------------------------------------------------
# Imports & Constants
# ------------------------------------------------------------------------------

import os

import requests
from utils import urljoin

MAX_SONG_RETURN = 10

GENIUS_HEADERS = {"Authorization": f"Bearer {os.environ.get('GENIUS_BEARER')}"}

GENIUS_BASE_URL = "https://api.genius.com/"

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


def query_artist_name(artist_id):
    artist_url = urljoin(GENIUS_BASE_URL, "artists", artist_id)
    artist_info = requests.get(artist_url, headers=GENIUS_HEADERS).json()

    return artist_info["response"]["artist"]["name"]


# --------------------------------------


def query_artist_songs(artist_id):
    songs_url = urljoin(
        GENIUS_BASE_URL,
        "artists",
        artist_id,
        "songs",
        sort="popularity",
        per_page=MAX_SONG_RETURN,
    )
    songs_info = requests.get(songs_url, headers=GENIUS_HEADERS)

    songs_info = songs_info.json()["response"]["songs"]
    return [song["title"] for song in songs_info]
