import azure.functions as func
import json
import uuid
import os
from azure.cosmos import CosmosClient

COSMOS_DB_URL = os.environ["COSMOS_DB_URL"]
COSMOS_DB_KEY = os.environ["COSMOS_DB_KEY"]
DATABASE_NAME = "ShortenerDB"
CONTAINER_NAME = "urls"

client = CosmosClient(COSMOS_DB_URL, COSMOS_DB_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def main(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    long_url = req_body.get("url")

    if not long_url:
        return func.HttpResponse("Invalid Request", status_code=400)

    short_code = str(uuid.uuid4())[:6]  # Generate a 6-character unique ID
    container.create_item({"id": short_code, "shortCode": short_code, "longUrl": long_url})

    return func.HttpResponse(json.dumps({"shortUrl": f"https://urlshortener-functions-new.azurewebsites.net/api/{short_code}"}), status_code=200)
