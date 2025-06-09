# Stock Identifier

This repository contains a small script that queries the [Financial Modeling Prep](https://financialmodelingprep.com/) API for companies releasing earnings on the current day and prints those that beat their EPS estimates.

## Setup

1. Create a `.env` file based on `env.example` and add your FMP API key:

   ```
   cp env.example .env
   # Edit .env and set FMP_API_KEY
   ```

2. Install dependencies:

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

The Financial Modeling Prep API offers a free tier for limited requests. You can obtain an API key by creating an account on their website.
