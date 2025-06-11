# Stock Identifier

This repository contains a small script that queries Nasdaq's unofficial earnings calendar and earnings surprise endpoints (via a read-only proxy) to print companies reporting today that beat their EPS estimates. No API key is required.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script to check today's earnings:

```bash
python positive_earnings.py
```

The script outputs all companies whose reported EPS is greater than the estimated EPS for today. If no companies beat expectations, it will state so.

## Notes

Data is fetched from Nasdaq's public endpoints using a proxy service. These endpoints are not officially supported and may change without notice.
