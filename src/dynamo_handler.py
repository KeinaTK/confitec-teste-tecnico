# ------------------------------------------------------------------------------
# Imports & Constants
# ------------------------------------------------------------------------------

import os
import uuid

import boto3

DYNAMODB_CONF = dict(
    # Defaults to amazon/dynamodb-local
    endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", "http://dynamodb:8000"),
    region_name=os.environ.get("REGION_NAME", ""),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", ""),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
    aws_session_token=os.environ.get("AWS_SESSION_TOKEN", ""),
)

dynamodb_client = boto3.client("dynamodb", **DYNAMODB_CONF)
dynamodb_resource = boto3.resource("dynamodb", **DYNAMODB_CONF)

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


def create_database():
    dynamodb_resource.create_table(
        TableName="Book_Songs",
        KeySchema=[
            {"AttributeName": "artistId", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "artistId", "AttributeType": "N"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )


# --------------------------------------


def detail_artist(artist_id: int) -> "dict | None":
    table = dynamodb_resource.Table("Book_Songs")
    response = table.get_item(Key={"artistId": artist_id})

    return response.get("Item", None)


# --------------------------------------


def create_artist(artist_id: int, name: str, songs: list[str]) -> dict:
    table = dynamodb_resource.Table("Book_Songs")

    item = {
        "artistId": artist_id,
        "uuid": str(uuid.uuid4()),
        "name": name,
        "songs": songs,
    }

    table.put_item(Item=item)

    return item


# --------------------------------------

if __name__ == "__main__":
    create_database()
