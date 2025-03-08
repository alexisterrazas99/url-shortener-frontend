import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        # Handle preflight requests
        return func.HttpResponse(
            "",
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )

    req_body = req.get_json()
    long_url = req_body.get("url")

    if not long_url:
        return func.HttpResponse("Invalid Request", status_code=400)

    short_code = "abc123"  # Replace with real short URL logic
    short_url = f"https://urlshortener-functions-new.azurewebsites.net/api/{short_code}"

    return func.HttpResponse(
        json.dumps({"shortUrl": short_url}),
        status_code=200,
        mimetype="application/json",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
    )
