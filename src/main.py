#!/bin/python3

import multiprocessing
import os

import requests
from cache.config import RedisConfig
from data.dynamo_handler import create_artist, create_database, detail_artist
from flask import Flask, request
from flask_caching import Cache
from utils import urljoin

MAX_SONG_RETURN = 10

app = Flask(__name__)
app.config.from_object(RedisConfig)
redis = Cache(app)

GENIUS_HEADERS = {"Authorization": f"Bearer {os.environ.get('GENIUS_BEARER')}"}

GENIUS_BASE_URL = "https://api.genius.com/"


def skip_cache_if_user_requested():
    use_cache = request.args.get("cache", "").lower() != "false"
    return not use_cache


@app.route("/artists/<int:artist_id>/")
@app.route("/artists/<int:artist_id>/songs/", methods=["GET"])
@redis.cached(timeout=60 * 24 * 7, unless=skip_cache_if_user_requested)
def get_artist_songs(artist_id):

    use_cache = request.args.get("cache", "").lower() != "false"

    if not use_cache:
        redis.clear()

    if not use_cache or (artist := detail_artist(artist_id)) is None:
        artist_name = query_artist_name(artist_id)
        artist_songs = query_artist_songs(artist_id)

        artist = create_artist(artist_id, artist_name, artist_songs)

    return artist


def query_artist_name(artist_id):
    artist_url = urljoin(GENIUS_BASE_URL, "artists", artist_id)
    artist_info = requests.get(artist_url, headers=GENIUS_HEADERS).json()

    return artist_info["response"]["artist"]["name"]


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


if __name__ == "__main__":

    if multiprocessing.current_process().pid > 1:
        create_database()

        if os.environ.get("FLASK_DEBUG"):
            import debugpy

            debugpy.listen(("0.0.0.0", 5137))
            print("Remote debugger attached - Docker container")

    app.run(host="0.0.0.0")
