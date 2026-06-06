# opensearch-indices-check

A lightweight Python script that fetches the list of indices from an OpenSearch
cluster and posts the report to a webhook (e.g. a Slack workflow trigger). It's
designed to be run on a schedule so you get a regular, sorted snapshot of your
indices and their storage usage.

## What it does

1. Queries the OpenSearch `_cat/indices` API using HTTP basic auth.
2. Receives the indices listing as plain text (sorted by store size, descending).
3. Sends the report as a JSON payload to a configured webhook URL.

## How it works

The logic lives in `main.py`:

- `fetch_indices()` calls the `OPENSEARCH_URL` endpoint with the configured
  credentials and returns the raw `_cat/indices` response text.
- `send_to_webhook(index_info)` posts the report (along with an auth `TOKEN`) to
  `WEBHOOK_URL`.
- `main()` ties the two together and prints progress to the console.

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`:
  - `requests`
  - `python-dotenv`

## Setup

1. Install the dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with the following variables:

```bash
# OpenSearch endpoint. Point this at the _cat/indices API.
# The query params below sort by store size, descending, with column headers.
OPENSEARCH_URL=https://your-opensearch-domain/_cat/indices?v&s=store.size:desc

# OpenSearch basic-auth credentials
OPENSEARCH_USERNAME=your-username
OPENSEARCH_PASSWORD=your-password

# Webhook to receive the report (e.g. a Slack workflow trigger URL)
WEBHOOK_URL=https://hooks.slack.com/triggers/XXXX/XXXX/XXXX

# Token forwarded in the webhook payload for verification/auth
TOKEN=your-webhook-token
```

> **Note:** Never commit your real `.env` file. Keep credentials and tokens out
> of version control.

## Usage

Run the script directly:

```bash
python main.py
```

Expected output:

```text
Fetching OpenSearch indices...
Sending report to webhook...
Webhook response: 200
Done
```

## Scheduling

To get periodic reports, run the script on a schedule using a cron job (Linux/macOS)
or Task Scheduler (Windows). For example, a daily cron entry at 9 AM:

```bash
0 9 * * * cd /path/to/opensearch-indices-check && /usr/bin/python main.py
```
