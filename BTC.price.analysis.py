import requests
from datetime import datetime
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.style.use('ggplot')
from matplotlib.pyplot import figure
import seaborn as sns
import mplfinance as mpf


response_ftmusd = requests.get("https://api.kraken.com/0/public/OHLC?pair=FTMUSD&since=1654041600&interval=1440")
response_btcusd = requests.get("https://api.kraken.com/0/public/OHLC?pair=xbtusd&since=1654041600&interval=1440")

def kraken_data_ftm_usd():
    global df_ftmusd, kraken_data_ftmusd
    kraken_data_ftmusd = response_ftmusd.json()
    df = pd.DataFrame(kraken_data_ftmusd["result"])
    df_ftmusd = pd.DataFrame(df['FTMUSD'].to_list(), columns=['timestamp', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'trades'])

    desired_width=320
    pd.set_option('display.width', desired_width)
    np.set_printoptions(linewidth=desired_width)
    pd.set_option('display.max_columns',10)
    pd.set_option('max_colwidth', 120)
    df_ftmusd['timestamp'] = pd.to_datetime(df_ftmusd['timestamp'], unit='s')
    df_ftmusd[df_ftmusd.columns[1:7]] = df_ftmusd[df_ftmusd.columns[1:7]].astype('float')
    # Calculating the pct change between opening and closing price for each day FTMUSD.
    df_ftmusd['%_price_change'] = ((df_ftmusd['close'] - df_ftmusd['open']) / df_ftmusd['open']) * 100
    print(df_ftmusd)

kraken_data_ftm_usd()


def kraken_data_btc_usd():

    global df_btcusd, kraken_data_btcusd
    kraken_data_btcusd = response_btcusd.json()
    df = pd.DataFrame(kraken_data_btcusd["result"])
    df_btcusd = pd.DataFrame(df['XXBTZUSD'].to_list(), columns=['timestamp', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'trades'])

    desired_width=320
    pd.set_option('display.width', desired_width)
    np.set_printoptions(linewidth=desired_width)
    pd.set_option('display.max_columns',10)
    pd.set_option('max_colwidth', 120)
    df_btcusd['timestamp'] = pd.to_datetime(df_btcusd['timestamp'], unit='s')
    df_btcusd[df_btcusd.columns[1:7]] = df_btcusd[df_btcusd.columns[1:7]].astype('float')
    #Calculating the pct change between opening and closing price for each day BTCUSD.
    df_btcusd['%_price_change'] = ((df_btcusd['close'] - df_btcusd['open']) / df_btcusd['open']) * 100
    print(df_btcusd)


kraken_data_btc_usd()

def percent_price_change():

    # Visualization of the pct change between opening and closing price for each day - FTMUSD.

    df_ftmusd.index = pd.DatetimeIndex(df_ftmusd['timestamp'])
    mpf.plot(df_ftmusd, type='candle', volume=True, style='yahoo', title='FTM/USD data 2022')
    plt.show()
    y = df_ftmusd['%_price_change']
    color = (y > 0).apply(lambda x: 'g' if x else 'r')
    plt.bar(df_ftmusd['timestamp'], y, color=color)
    plt.xlabel("Time")
    plt.ylabel("Price Change in %")
    plt.title("FTM/USD Price Change in %")
    plt.show()

    #Visualization of the pct change between opening and closing price for each day - BTCUSD.

    df_btcusd.index = pd.DatetimeIndex(df_btcusd['timestamp'])
    mpf.plot(df_btcusd, type='candle', volume=True, style='yahoo', title='Bitcoin data 2022')
    plt.show()
    y = df_btcusd['%_price_change']
    color = (y > 0).apply(lambda x: 'g' if x else 'r')
    plt.bar(df_btcusd['timestamp'], y, color=color)
    plt.xlabel("Time")
    plt.ylabel("Price Change in %")
    plt.title("BTC Price Change in %")
    plt.show()

percent_price_change()


def correlations():

    df3 = pd.concat([df_btcusd['%_price_change'], df_ftmusd['%_price_change']], axis=1, keys=['%_change_btc', '%_change_ftm'])
    df3['timestamp'] = df_ftmusd['timestamp']
    col = df3.pop('timestamp')
    df3.insert(0, col.name, col)
    print(df3)

    cor = df3.corr(numeric_only=True)
    sns.heatmap(cor, annot=True)
    plt.title('Correlation Matrix for BTC FTM')
    plt.xlabel('BTC')
    plt.ylabel('FTM')
    plt.show()

    plt.plot(df3['timestamp'], df3['%_change_btc'], df3['timestamp'], df3['%_change_ftm'])
    plt.legend(labels=['Change BTC in %', 'change FTM in %'])
    plt.show()

    print(cor)
correlations()