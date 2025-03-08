import azure.functions as func
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
    short_code = req.route_params.get("short_code")

    url_data = container.query_items(
        query="SELECT * FROM c WHERE c.shortCode=@shortCode",
        parameters=[{"name": "@shortCode", "value": short_code}],
        enable_cross_partition_query=True
    )

    url_data = list(url_data)
    if not url_data:
        return func.HttpResponse("URL Not Found", status_code=404)

    long_url = url_data[0]["longUrl"]
    return func.HttpResponse(status_code=301, headers={"Location": long_url})
