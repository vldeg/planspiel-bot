from portfolio import Portfolio
from api import APIProvider
from dashboard import dashboard
from db import OrderRecord
from rich.console import Console
from rich.live import Live
from loguru import logger

import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
import config
import db

console = Console(record=True)

def run_daily_scan():
    logger.info("Starting daily scan...")
    data = yf.download(
        config.TICKERS,
        period="2y",
        interval="1d",
        auto_adjust=True,
        group_by="ticker",
        progress=True
    )
    eur_to_usd = yf.download(
        "EURUSD=X",
        period="1d",
        interval="1m",
        progress=False
    )

    eur_to_usd_rate = float(eur_to_usd["Close"].dropna().iloc[-1].item())

    df = data.stack(level=0, future_stack=True)
    df.index.names = ["Date", "Ticker"]
    df = df.swaplevel(0, 1).sort_index()

    def indicators(group):
        group.ta.sma(length=50, append=True)
        group.ta.sma(length=130, append=True)
        group.ta.sma(length=200, append=True)
        group.ta.atr(length=14, append=True)
        group.ta.donchian(lower_length=20, higher_length=20, append=True)

        group["VMA20"] = group["Volume"].rolling(20).mean().shift(1)
        group["Donchian_High20"] = group["DCU_20_20"].shift(1)
        group["RSL"] = (
            group["Close"] / group["SMA_130"]
        )

        return group
    
    final = df.groupby("Ticker", group_keys=False).apply(indicators)
    latest = final.groupby(level="Ticker").tail(1)
    latest = latest.reset_index()

    watchlist = latest[
        (latest["Close"] > latest["SMA_50"]) &
        (latest["SMA_50"] > latest["SMA_200"])
    ].copy()
    watchlist = watchlist.sort_values(by="RSL", ascending=False)

    watchlist["Buy"] = (
        (watchlist["Close"] > watchlist["Donchian_High20"] + 0.3 * watchlist["ATRr_14"]) &
        (watchlist["Volume"] > 1.6 * watchlist["VMA20"])
    )

    stocks = watchlist[watchlist["Buy"] == True].to_dict(orient="records")

    api = APIProvider(base_url=config.API_BASE_URL)
    api.authorize()

    depot = api.get_portfolio_stats(config.PORTFOLIO_ID)
    depot_items = api.get_portfolio_items(config.PORTFOLIO_ID)
    depot_isins = {item["isin"] for item in depot_items}
    equity = depot["equity"]
    available_cash = depot["available_cash"]

    p = Portfolio(equity, available_cash)
    generated_orders = []

    with Live(
        dashboard(
            equity,
            available_cash,
            eur_to_usd_rate,
            len(stocks),
            len(config.TICKERS),
            depot["performance"],
            generated_orders
        ),
        refresh_per_second=3,
        console=console
    ) as live:
        for stock in stocks:
            ticker = stock["Ticker"]

            try:
                isin = yf.Ticker(stock["Ticker"]).get_isin()
            except Exception:
                logger.exception("Failed to retrieve ISIN for {ticker}", ticker=ticker)
                continue

            if not isin:
                logger.warning("No ISIN found for {ticker}. Skipping...", ticker=ticker)
                continue

            if isin in depot_isins:
                logger.warning("Stock {ticker} ({isin}) is already in the portfolio. Skipping...", ticker=ticker, isin=isin)
                continue

            levels = p.calculate_limit_and_stop_loss(
                stock["Close"], 
                stock["ATRr_14"],
                eur_to_usd_rate
            )
            order = p.calculate_position_size(
                levels["limit"],
                levels["stop_loss"]
            )
            if not order:
                logger.warning("Out of available cash. Stopping orders.")
                break

            try:
                res = api.place_buy_order(config.PORTFOLIO_ID, isin, order["amount"], levels["limit"])
                if not res or res.get("success") is not True:
                    logger.error("API denied a BUY order for {ticker} ({isin}) with status code {code}",
                             ticker=ticker, isin=isin, code=res["status_code"])
                    continue
            except Exception:
                logger.exception("Failed to place a BUY order for {ticker} ({isin})", ticker=ticker, isin=isin)
                continue

            available_cash = order["available_cash"]
            generated_orders.append({
                "ticker": ticker,
                "isin": isin,
                "amount": order["amount"],
                "order_volume": order["order_volume"],
                "limit": levels["limit"],
                "stop_loss": levels["stop_loss"],
                "total_fees": order["total_fees"]
            })
            db.create_order(
                OrderRecord(
                    isin=isin,
                    name=ticker,
                    amount=order["amount"],
                    order_volume=order["order_volume"],
                    stop_loss=levels["stop_loss"],
                    limit=levels["limit"]
                )
            )
            live.update(
                dashboard(
                    equity,
                    available_cash,
                    eur_to_usd_rate,
                    len(stocks),
                    len(config.TICKERS),
                    depot["performance"],
                    generated_orders
                )
            )

    watchlist.to_csv("data/watchlist.csv", index=False, decimal=",", encoding="utf-8-sig")
    logger.success("Scan completed, {count} new orders placed.", count=len(generated_orders))
