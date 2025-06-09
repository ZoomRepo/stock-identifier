import os
import requests
from datetime import date

API_URL = "https://financialmodelingprep.com/api/v3/earning_calendar"
API_KEY = os.getenv("FMP_API_KEY")


def fetch_earnings(target_date: date):
    if API_KEY is None:
        raise RuntimeError("FMP_API_KEY environment variable not set")

    params = {
        "from": target_date.isoformat(),
        "to": target_date.isoformat(),
        "apikey": API_KEY,
    }
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def filter_positive_earnings(items):
    positive = []
    for item in items:
        eps = item.get("eps")
        eps_est = item.get("epsEstimated")
        if eps is None or eps_est is None:
            continue
        if eps > eps_est:
            positive.append(item)
    return positive


def main():
    today = date.today()
    earnings = fetch_earnings(today)
    winners = filter_positive_earnings(earnings)
    if not winners:
        print(f"No positive earnings found for {today}")
        return
    print(f"Positive earnings for {today}:")
    for item in winners:
        symbol = item.get("symbol")
        eps = item.get("eps")
        eps_est = item.get("epsEstimated")
        print(f"{symbol}: EPS {eps} beats estimate {eps_est}")


if __name__ == "__main__":
    main()
