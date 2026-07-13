"""Daily market pulse: fetch major US index quotes and version them in git.

Runs unattended on GitHub Actions every weekday. Appends one row per index
to data/history.csv and refreshes the Latest section of README.md.
Stdlib only, no dependencies, nothing to break.
"""

import csv
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SYMBOLS = {
    "^GSPC": "S&P 500",
    "^IXIC": "Nasdaq Composite",
    "^DJI": "Dow Jones",
    "^VIX": "VIX",
    "^TNX": "10-Year Treasury Yield",
}
CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1d&interval=1d"
USER_AGENT = "Mozilla/5.0 (market-pulse; +https://github.com/maupatel/market-pulse)"
HISTORY = Path("data/history.csv")
README = Path("README.md")
MARKER_START = "<!-- pulse:start -->"
MARKER_END = "<!-- pulse:end -->"


def fetch_quotes():
    quotes = []
    for symbol, name in SYMBOLS.items():
        url = CHART_URL.format(symbol=urllib.parse.quote(symbol))
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
        result = payload["chart"]["result"][0]
        meta = result["meta"]
        price = meta.get("regularMarketPrice")
        if price is None:
            continue
        session = datetime.fromtimestamp(
            meta["regularMarketTime"], tz=timezone.utc
        ).strftime("%Y-%m-%d")
        quotes.append(
            {
                "fetched_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
                "symbol": symbol,
                "name": name,
                "date": session,
                "close": round(price, 2),
                "prev_close": meta.get("chartPreviousClose"),
            }
        )
    return quotes


def append_history(quotes):
    HISTORY.parent.mkdir(exist_ok=True)
    new_file = not HISTORY.exists()
    with HISTORY.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(quotes[0].keys()))
        if new_file:
            writer.writeheader()
        writer.writerows(quotes)


def update_readme(quotes):
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [MARKER_START, f"_Last run: {stamp}_", ""]
    lines += ["| Index | Session date | Close |", "|---|---|---|"]
    for q in quotes:
        lines.append(f"| {q['name']} | {q['date']} | {q['close']} |")
    lines.append(MARKER_END)
    block = "\n".join(lines)

    text = README.read_text(encoding="utf-8")
    start = text.index(MARKER_START)
    end = text.index(MARKER_END) + len(MARKER_END)
    README.write_text(text[:start] + block + text[end:], encoding="utf-8")


def main():
    quotes = fetch_quotes()
    if not quotes:
        raise SystemExit("No quotes returned; leaving repo untouched.")
    append_history(quotes)
    update_readme(quotes)
    print(f"Recorded {len(quotes)} quotes.")


if __name__ == "__main__":
    main()
