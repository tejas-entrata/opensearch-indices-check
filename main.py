import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENSEARCH_URL = os.getenv("OPENSEARCH_URL")
OPENSEARCH_USERNAME = os.getenv("OPENSEARCH_USERNAME")
OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
TOKEN = os.getenv("TOKEN")


def fetch_indices():
    response = requests.get(
        OPENSEARCH_URL,
        auth=(OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD),
        timeout=30,
    )

    response.raise_for_status()

    return response.text


def send_to_webhook(index_info):
    payload = {
        "index_info": index_info,
        "token": TOKEN,
    }

    response = requests.post(
        WEBHOOK_URL,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    return response


def main():
    print("Fetching OpenSearch indices...")

    index_info = fetch_indices()

    print("Sending report to webhook...")

    response = send_to_webhook(index_info)

    print(f"Webhook response: {response.status_code}")
    print("Done")


if __name__ == "__main__":
    main()
