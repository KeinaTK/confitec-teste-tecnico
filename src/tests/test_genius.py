import json
import unittest

import responses

from genius_client import (
    GENIUS_BASE_URL,
    MAX_SONG_RETURN,
    query_artist_name,
    query_artist_songs,
)
from utils import urljoin


class TestGeniusClient(unittest.TestCase):
    def setUp(self):
        self.artist_id = 16775

    def mock_get_artists_genius(self, request):
        print("CALLED THE MOCKED THING")
        response = {
            "response": {
                "artist": {
                    "alternate_names": "name",
                    "api_path": "/artists/16775",
                    "description": "description",
                    "facebook_name": "SiaMusic",
                    "followers_count": 1315,
                    "header_image_url": "https://images.genius.com/570d01b6da3e0d9f5abc5ddaebdd6825.1000x989x1.jpg",
                    "id": 16775,
                    "image_url": "https://images.genius.com/aba931aaf48b7728f3f4869b13eb9741.1000x1000x1.jpg",
                    "instagram_name": "SiaMusic",
                    "is_meme_verified": False,
                    "is_verified": True,
                    "name": "Sia",
                    "translation_artist": False,
                    "twitter_name": None,
                    "url": "https://genius.com/artists/Sia",
                    "current_user_metadata": "current_user_metadata",
                    "iq": 8513,
                    "description_annotation": "",
                    "user": "",
                }
            }
        }

        return 200, {}, json.dumps(response)

    @responses.activate
    def test_query_artist_name(self):

        artist_url = urljoin(GENIUS_BASE_URL, "artists", self.artist_id)

        responses.add_callback(
            responses.GET,
            artist_url,
            callback=self.mock_get_artists_genius,
            content_type="application/json",
        )

        name = query_artist_name(16775)

        assert responses.calls[0].response.status_code == 200
        assert name == "Sia"

    def mock_get_genius_artists_songs(self, request):
        response = {
            "response": {
                "songs": [
                    {
                        "annotation_count": 4,
                        "api_path": "/songs/6374199",
                        "artist_names": "Sia",
                        "full_title": "1+1 by Sia",
                        "header_image_thumbnail_url": "https://images.genius.com/d2ba123f26df847c6485a9d4a217deb5.300x300x1.png",
                        "header_image_url": "https://images.genius.com/d2ba123f26df847c6485a9d4a217deb5.1000x1000x1.png",
                        "id": 6374199,
                        "lyrics_owner_id": 8901159,
                        "lyrics_state": "complete",
                        "path": "/Sia-1-1-lyrics",
                        "pyongs_count": 1,
                        "relationships_index_url": "https://genius.com/Sia-1-1-sample",
                        "release_date_for_display": "February 12, 2021",
                        "song_art_image_thumbnail_url": "https://images.genius.com/d2ba123f26df847c6485a9d4a217deb5.300x300x1.png",
                        "song_art_image_url": "https://images.genius.com/d2ba123f26df847c6485a9d4a217deb5.1000x1000x1.png",
                        "title": "1+1",
                        "title_with_featured": "1+1",
                        "url": "https://genius.com/Sia-1-1-lyrics",
                    }
                ]
            }
        }

        return 200, {}, json.dumps(response)

    @responses.activate
    def test_query_artist_songs(self):

        songs_url = urljoin(
            GENIUS_BASE_URL,
            "artists",
            self.artist_id,
            "songs",
            sort="popularity",
            per_page=MAX_SONG_RETURN,
        )

        responses.add_callback(
            responses.GET,
            songs_url,
            callback=self.mock_get_genius_artists_songs,
            content_type="application/json",
        )

        resp = query_artist_songs(16775)

        assert responses.calls[0].response.status_code == 200
        assert resp == ["1+1"]
