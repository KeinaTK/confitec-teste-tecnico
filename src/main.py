#!/bin/python3

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import multiprocessing
import os

import dynamo_handler
import genius_client
from flask import Flask, request
from flask_caching import Cache
from redis_config import RedisConfig

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


def parse_cache_querystring() -> bool:
    """Utility function to parse the `cache` querystring parameter"""
    return request.args.get("cache", "").lower() != "false"


# --------------------------------------


def skip_cache_if_user_requested() -> bool:
    """This function returns whether to hit the Redis Cache or not. The checking
    is realized via the `cache` querystring, which should be:
        - False, if the user doesn't want to hit cache, or
        - Empty|Anything else, if the user desires caching.
    """
    return not parse_cache_querystring()


# ------------------------------------------------------------------------------
# Application Setup
# ------------------------------------------------------------------------------

app = Flask(__name__)

# Redis configuration. Gets values from .env file
app.config.from_object(RedisConfig)
redis = Cache(app)

# Endpoints --------------------------------------------------------------------


@app.route("/artists/<int:artist_id>/")
@app.route("/artists/<int:artist_id>/songs/", methods=["GET"])
@redis.cached(timeout=60 * 24 * 7, unless=skip_cache_if_user_requested)
def get_artist_songs(artist_id):

    use_cache = parse_cache_querystring()

    if not use_cache:
        redis.clear()

    if not use_cache or (artist := dynamo_handler.detail_artist(artist_id)) is None:
        artist_name = genius_client.query_artist_name(artist_id)
        artist_songs = genius_client.query_artist_songs(artist_id)

        artist = dynamo_handler.create_artist(artist_id, artist_name, artist_songs)

    return artist


# --------------------------------------

if __name__ == "__main__":

    if multiprocessing.current_process().pid > 1:
        dynamo_handler.create_database()

        if os.environ.get("FLASK_DEBUG"):
            import debugpy

            debugpy.listen(("0.0.0.0", 5137))
            print("Remote debugger attached - Docker container")

    app.run(host="0.0.0.0")
