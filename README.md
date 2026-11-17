# market-pulse

![Daily pulse](https://github.com/maupatel/market-pulse/actions/workflows/daily.yml/badge.svg)

A fully automated daily data pipeline, end to end, with zero manual steps:

1. **Ingest**: GitHub Actions wakes up every weekday morning and pulls closing quotes for the S&P 500, Nasdaq 100, and Dow Jones.
2. **Transform**: quotes are normalized and appended to a versioned CSV history.
3. **Serve**: the table below refreshes automatically, and the full history lives in [`data/history.csv`](data/history.csv).

No servers, no credentials, no dependencies. Python stdlib + cron + git as the storage layer. Every green square on my contribution graph from this repo is the pipeline proving it ran.

## Latest

<!-- pulse:start -->
_Last run: 2026-11-17 21:51 UTC_

| Index | Session date | Close | Change |
|---|---|---|---|
| S&P 500 | 2026-11-17 | 7340.53 | 🔻 -1.03% |
| Nasdaq Composite | 2026-11-17 | 24328.38 | 🔻 -0.74% |
| Dow Jones | 2026-11-17 | 50759.42 | 🔻 -1.64% |
| VIX | 2026-11-17 | 25.46 | 🔺 +11.13% |
| 10-Year Treasury Yield | 2026-11-17 | 5.1 | 🔻 -0.41% |
<!-- pulse:end -->

## Why this exists

Small enough to read in five minutes, real enough to demonstrate the whole discipline: scheduling, idempotent runs, data versioning, and self-updating documentation.

Built and maintained by [Maulik Patel](https://github.com/maupatel), Senior Data Analyst at Capital One.
