# Portfolio Tracker

A desktop portfolio tracker built with PyQt5. Users can register and log in, manage
assets, view market data and financial news, set price alerts, and see portfolio
insights with charts.

## Features

- User registration and login (SQLite, SHA-256 hashed passwords)
- Add, view, modify and delete portfolio assets
- Live stock data and charts (yfinance + matplotlib)
- Financial news feed (NewsAPI)
- Price alerts with desktop notifications
- Portfolio insights and analysis

## Setup

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your [NewsAPI](https://newsapi.org) key:

```
NEWS_API_KEY=your_newsapi_key_here
```

## Running

```bash
python main.py
```

The SQLite database is created automatically on first run.

## Project structure

```
main.py             Entry point
GUI/                PyQt5 windows and tabs
Logic/              News fetching, alert system
Database/           SQLite schema and data access
Assets/             Stylesheets
```
