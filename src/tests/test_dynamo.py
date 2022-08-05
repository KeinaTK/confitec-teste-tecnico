import unittest
import uuid
from dataclasses import dataclass

import pytest

from dynamo_handler import (
    create_artist,
    create_database,
    detail_artist,
    dynamodb_resource,
)


class TestDynamoHandler(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, mocker):
        self.mocker = mocker

    def test_create_database(self):
        patched_create_table = self.mocker.patch.object(
            dynamodb_resource, "create_table"
        )

        create_database()

        patched_create_table.assert_called_once_with(
            TableName="Book_Songs",
            KeySchema=[
                {"AttributeName": "artistId", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "artistId", "AttributeType": "N"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

    def test_detail_artist_with_existing_artist(self):
        @dataclass
        class FakeTable:
            artist_id: int

            def get_item(self, *, Key):
                assert self.artist_id == Key["artistId"]
                return {"Item": "mocked_item"}

        fake_table = FakeTable(1337)
        patched_table = self.mocker.patch.object(dynamodb_resource, "Table")
        patched_table.return_value = fake_table

        artist = detail_artist(fake_table.artist_id)

        patched_table.assert_called_once_with("Book_Songs")

        assert artist == "mocked_item"

    def test_detail_artist_with_nonexisting_artist(self):
        @dataclass
        class FakeTable:
            artist_id: int

            def get_item(self, *, Key):
                assert self.artist_id == Key["artistId"]
                return {}

        fake_table = FakeTable(1337)
        patched_table = self.mocker.patch.object(dynamodb_resource, "Table")
        patched_table.return_value = fake_table

        artist = detail_artist(fake_table.artist_id)

        patched_table.assert_called_once_with("Book_Songs")

        assert artist is None

    def test_create_artist(self):

        put_item_was_called = False

        @dataclass
        class FakeTable:
            artist_id: int
            name: str
            songs: list[str]

            def put_item(self, *, Item):
                nonlocal put_item_was_called
                put_item_was_called = True

                assert self.artist_id == Item["artistId"]
                assert self.name == Item["name"]
                assert self.songs == Item["songs"]

                try:
                    uuid.UUID(Item["uuid"])
                    assert True

                except ValueError:
                    assert False, "Item['uuid'] is not a valid UUID"

        fake_table = FakeTable(
            1337, "The Artist", ["A hit song", "That other song noone heard about"]
        )

        patched_table = self.mocker.patch.object(dynamodb_resource, "Table")
        patched_table.return_value = fake_table

        create_artist(fake_table.artist_id, fake_table.name, fake_table.songs)

        patched_table.assert_called_once_with("Book_Songs")

        assert put_item_was_called, "Method `table.put_item()` wasn't called"
