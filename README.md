# Robinhood Crypto Trading Bot
A simple Python crypto algotrader 

## Introduction
I've been wanting to play around with algotraders for a while now. After some initial research, I stumbled upon [Jason Bowling's article](https://medium.com/swlh/a-full-crypto-trading-bot-in-python-aafba122bc4e), in which he describes the mechanics of his rudimentary Python bot. His code tickled my curiosity, so I started tinkering with it. In the spirit of open source, I created this public repository to share my experiments with anyone interested in such esoteric stuff.

## Disclaimer
To use Jason's words: cryptocurrency investing is *risky*! Doing it using a computer program is even riskier. Doing it with code you didn’t write is a _terrible_ idea. What you do with this code is entirely up to you, and any risks you take are your own. It’s intended to be educational and comes with absolutely no guarantee of anything at all. You could lose all your money. Seriously.

## Installation
You'll need access to a working Python3 interpreter. For the sake of simplicity, I am going to assume that you know your way around a Linux shell, and that you have [pip3](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/#installing-pip-for-python-3) on your machine. Install the following dependencies:
* [Robin-Stock](http://www.robin-stocks.com/en/latest/quickstart.html): `pip3 install robin_stocks`
* [Pandas](https://pandas.pydata.org/pandas-docs/stable/index.html): `pip3 install pandas`
* [TA-Lib](https://www.ta-lib.org/): download their tarball and compile it

Once you have all the dependencies in place, clone this repo somewhere on your machine, copy `config-sample.py` to `config.py`, and edit it to enter at least your Robinhood username and password. You can also use the following settings to customize the bot's behavior:
* (string) `username` and `password`: Robinhood credentials
* (bool) `trades_enabled`:  If False, run in test mode and just collect data, otherwise submit orders
* (bool) `simulate_api_calls`: Simulate connections to Kraken and Robinhood APIs (by generating random values for all API calls)
* (list) `ticker_list`: List of coin ticker pairs Kraken/Robinhood (XETHZUSD/ETH, etc); see [here](https://api.kraken.com/0/public/AssetPairs) for a complete list of available tickers on Kraken
* (dict) `trade_signals`: Select which strategies to use (buy, sell); see _signals.py_ for a list of available methods (omit the *buy_*/*sell_* method prefix when passing the value here: buy_sma_crossover_rsi -> sma_crossover_rsi)
* (float) `buy_below_moving_average`: If the price dips below the MA by this percentage, and if the RSI is below the oversold threshold (see below), it will try to buy
* (float) `sell_above_buy_price`: Once the price rises above the Buy price by this percentage, it will try to sell
* (float) `buy_amount_per_trade`: If greater than zero, buy this amount of coin, otherwise use all the cash in the account
* (dict) `moving_average_periods`: Number of MA observations to wait before sprinting into action, for each measure (SMA fast, SMA slow, MACD fast, MACD slow, MACD signal)
* (int) `rsi_period`: Length of the observation window for calculating the RSI
* (float) `rsi_buy_threshold`: Threshold below which the bot will try to buy
* (float) `reserve`: By default, the bot will try to use all the funds available in your account to buy crypto; use this value if you want to set aside a given amount that the bot should not spend
* (float) `stop_loss_threshold`: Threshold below which the bot will sell its holdings, regardless of any gains
* (int) `minutes_between_updates`: How often should the bot spring into action (1 (default), 5, 15, 30, 60, 240, 1440, 10080, 21600)
* (bool) `save_charts`: Enable this feature to have the bot save SMA charts for each coin it's handling
* (int) `max_data_rows`: Max number of data points to store in the Pickle file (if you have issues with memory limits on your machine). 1k rows = 70kB

## Running the bot
I've included a simple Bash utility script to start, stop and check the bot's status:

* `./bot.sh start` will run the bot in the background (even after you close your terminal window)
* `./bot.sh stop` will stop the background process
* `./bot.sh restart` will reload the bot (useful if you've changed its configuration, and want to load the new values)
* `./bot.sh status` will tell you if the bot is currently running or not

The overall flow looks like this:
* Load the configuration and initialize or load a previously saved state
* Load saved data points or download new ones from Kraken
* Every 5 minutes (you can customize this in the settings), download the latest price info from Kraken for each coin
* Compute [moving averages](https://www.investopedia.com/terms/m/movingaverage.asp) and [RSI](https://www.investopedia.com/terms/r/rsi.asp), making sure that there haven't been any interruptions in the data sequence
* If the conditions to buy or sell are met, submit the corresponding order
* Rinse and repeat

## Bot Status
A summary of each iteration is logged in `status.log`. The bot maintains a list of purchased assets (saved as `orders.pickle`) and at each iteration, it determines if the conditions to sell any of them are met. It also handles swing and miss orders, by checking if any of the orders placed during the previous iteration are still pending (not filled), and cancels them. The typical output should resemble this format:

```
-- Bot Status ---------------------------
Iteration completed on 2021-02-01 15:25
Buying power: $448.49
-- Data Snapshot ------------------------
             timestamp      ETH    ETH_SMA_F    ETH_SMA_S    ETH_RSI  ETH_MACD  ETH_MACD_S
1867  2021-02-01 15:09  1338.28  1330.445000  1319.163125  74.024414  4.163829    3.842706
1868  2021-02-01 15:14  1339.00  1331.281667  1319.811042  74.806159  4.450957    3.994769
1869  2021-02-01 15:19  1339.00  1332.134167  1320.424167  74.806159  4.625192    4.152375
1870  2021-02-01 15:24  1337.01  1333.000833  1321.011667  68.224578  4.550246    4.251843
1871  2021-02-01 15:25  1337.01  1333.640000  1321.655208  68.224578  4.439672    4.298800
-- Assets -------------------------------
ETH: 0.071683 | Price: $1395.03 | Cost: $100.0 | Current value: $95.841
ETH: 0.302484 | Price: $1322.38 | Cost: $399.999 | Current value: $404.424
```

The "Bot Status" section shows the available cash amount that can be used to buys new assets. Next you'll see a snapshot of the most recent data retrieved from Kraken, along with the corresponding indicators (SMA_F = fast SMA, SMA_S = slow SMA, etc), where the rolling period for each of them can be customized in the settings. Last but least, the "Assets" section, if present, lists all the purchased assets the bot is managing for you, along with their purchase price, cost and current value.

## Charts
How does the saying go? A picture is always worth a thousand words, ehm... data points. For each coin you track, a line chart will be refreshed at each iteration (and saved in the `charts` folder), summarizing the current state and the SMA indicators. 

![](charts/chart-eth-sma-demo.png)

## Indicators
### Relative Strength Index
The RSI trading indicator is a measure of the relative strength of the market (compared to its history), a momentum oscillator and is often used as an overbought and oversold technical indicator. The RSI is displayed as a line graph that moves between two extremes from 0 to 100. Traditional interpretation and usage of the RSI are that values of 70 or above indicate that a security is becoming overvalued and the price of the security is likely to go down in the future (bearish), while the RSI reading of 30 or below indicates an oversold or undervalued condition and the price of the security is likely to go up in the future (bullish).

### Moving Average Convergence/Divergence
Moving average convergence divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price. The MACD is calculated by subtracting the 26-period [exponential moving average](https://www.investopedia.com/terms/e/ema.asp) (EMA) from the 12-period EMA. The result of that calculation is the MACD line. A nine-day EMA of the MACD called the "signal line," is then plotted on top of the MACD line, which can function as a trigger for buy and sell signals. Traders may buy the security when the MACD crosses above its signal line and sell—or short—the security when the MACD crosses below the signal line. Moving average convergence divergence (MACD) indicators can be interpreted in several ways, but the more common methods are crossovers, divergences, and rapid rises/falls.

## Technical Analysis
This bot can implement any technical analysis as a series of conditions on the indicators it collects. Some of them are built into the algorithm, to give you a starting point to create your own. For example, Jason's approach is to buy when the price drops below the Fast-SMA by the percentage configured in the settings, and the RSI is below the threshold specified in the config file. By looking at multiple data points, you can also determine if a crossover happened, and act accordingly. The simple strategy outlined here above can be expanded [in many ways](https://medium.com/mudrex/rsi-trading-strategy-with-20-sma-on-mudrex-a26bd2ac039b). To that end, this bot keeps track of a few indicators that can be used to [determine if it's time to buy or sell](https://towardsdatascience.com/algorithmic-trading-with-macd-and-python-fef3d013e9f3): SMA fast, SMA slow, RSI, MACD, MACD Signal. Future versions will include ways to select which approach you would like to use. 

## Backtesting
Backtesting is the process of testing a trading or investment strategy using data from the past to see how it would have performed. For example, let's say your trading strategy is to buy Bitcoin when it falls 3% in a day, your backtest software will check Bitcoin's prices in the past and fire a trade when it fell 3% in a day. The backtest results will show if the trades were profitable. At this time, this bot doesn't offer an easy way to ingest past data and run simulations, but it's something I have on my wishlist for sure.

## Additional Notes
This code is *far* from perfect and can certainly be improved. Waking up and finding that the bot has made money for you while you were sleeping can be cool. Watching the price continue to plunge after the bot buys, not so much. Remember, there's no logic to try and locate the bottom of a dip. And that's, in a way, why I decided to publish these experiments here on Github: if you feel like lending a hand, submit a pull request, don't be shy!
