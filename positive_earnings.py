import requests
from datetime import date
import json

# Use Nasdaq's undocumented API via a read-only proxy to avoid API keys
CALENDAR_URL = (
    "https://r.jina.ai/https://api.nasdaq.com/api/calendar/earnings"
)
SURPRISE_URL = (
    "https://r.jina.ai/https://api.nasdaq.com/api/company/{symbol}/earnings-surprise"
)


def fetch_earnings(target_date: date):
    """Return the earnings calendar for a specific date."""
    params = {"date": target_date.isoformat()}
    resp = requests.get(CALENDAR_URL, params=params, timeout=10, headers={"User-Agent": "python"})
    resp.raise_for_status()
    text = resp.text
    start = text.find("{")
    data = json.loads(text[start:])
    return data.get("data", {}).get("rows", [])


def fetch_surprises(symbol: str):
    """Fetch historical earnings surprise data for a symbol."""
    url = SURPRISE_URL.format(symbol=symbol)
    resp = requests.get(url, timeout=10, headers={"User-Agent": "python"})
    resp.raise_for_status()
    text = resp.text
    start = text.find("{")
    data = json.loads(text[start:])
    payload = data.get("data") or {}
    table = payload.get("earningsSurpriseTable")
    if not table:
        return []
    return table.get("rows", [])


def filter_positive_earnings(target_date: date, calendar_rows):
    """Return items where reported EPS beats the estimate on the target date."""
    winners = []
    date_str = f"{target_date.month}/{target_date.day}/{target_date.year}"
    for entry in calendar_rows:
        symbol = entry.get("symbol")
        if not symbol:
            continue
        for surprise in fetch_surprises(symbol):
            if surprise.get("dateReported") != date_str:
                continue
            try:
                eps = float(surprise.get("eps"))
                est = float(surprise.get("consensusForecast"))
            except (TypeError, ValueError):
                break
            if eps > est:
                winners.append({"symbol": symbol, "eps": eps, "estimate": est})
            break
    return winners


def main():
    today = date.today()
    earnings = fetch_earnings(today)
    winners = filter_positive_earnings(today, earnings)
    if not winners:
        print(f"No positive earnings found for {today}")
        return
    print(f"Positive earnings for {today}:")
    for item in winners:
        symbol = item["symbol"]
        eps = item["eps"]
        eps_est = item["estimate"]
        print(f"{symbol}: EPS {eps} beats estimate {eps_est}")


if __name__ == "__main__":
    main()
