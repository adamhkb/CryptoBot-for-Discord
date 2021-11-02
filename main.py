import discord
from pycoingecko import CoinGeckoAPI
import pandas as pd
from datetime import datetime
import schedule
import plotly.express as px
from io import BytesIO


token = ''
client = discord.Client()

cg = CoinGeckoAPI()
db = ['bitcoin', 'ethereum', 'binancecoin', 'tether', 'cardano', 'solana', 'ripple', 'polkadot', 'shiba-inu', 'dogecoin', 'usd-coin', 'terra-luna', 'avalanche-2', 'wrapped-bitcoin', 'chainlink', 'binance-usd', 'litecoin', 'uniswap', 'matic-network', 'algorand', 'bitcoin-cash', 'cosmos', 'stellar', 'vechain', 'axie-infinity', 'dai', 'internet-computer', 'filecoin', 'fantom', 'tron', 'theta-token', 'ftx-token', 'ethereum-classic', 'compound-ether', 'hedera-hashgraph', 'staked-ether', 'okb', 'near', 'tezos', 'elrond-erd-2', 'crypto-com-chain', 'monero', 'the-graph', 'thorchain', 'eos', 'pancakeswap-token', 'flow', 'aave', 'klay-token', 'cdai', 'iota', 'olympus', 'compound-usd-coin', 'quant-network', 'decentraland', 'ecash', 'kusama', 'leo-token', 'harmony', 'bitcoin-cash-sv', 'neo', 'safemoon', 'terrausd', 'helium', 'waves', 'bitcoin-cash-abc-2', 'arweave', 'bittorrent-2', 'amp-token', 'huobi-btc', 'magic-internet-money', 'holotoken', 'enjincoin', 'chiliz', 'celo', 'maker', 'sushi', 'spell-token', 'compound-governance-token', 'omisego', 'dash', 'zcash', 'blockstack', 'theta-fuel', 'celsius-degree-token', 'havven', 'curve-dao-token', 'nem', 'huobi-token', 'qtum', 'icon', 'decred', 'nexo', 'the-sandbox', 'basic-attention-token', 'ecomi', 'kucoin-shares', 'zilliqa', 'secret', 'xdce-crowd-sale']
db = sorted(db)

def SupportedCrypto(crypto):
    if crypto in db:
        return True
    else:
        return(f"No information on {crypto.lower()} \n"
               f"Please try the following recognised cryptocurrencies: \n\n"
               f"{db}")

def graphCrypto(COIN, DAYS):
    data = cg.get_coin_ohlc_by_id(
        id=COIN, vs_currency='gbp', days=DAYS)
    time_stamp = []
    close = []
    for x in data:
        time_stamp.append((datetime.fromtimestamp(x[0]/1000)))
        close.append(x[4])
    df = pd.DataFrame(list(zip(time_stamp, close)),
                      columns=['Date', 'Close Price'])
    df['Date'] = pd.to_datetime(df['Date'])
    fig = px.line(df, x="Date", y="Close Price")
    if DAYS == 1:
        duration = "24 Hours"
        filename = f"Time Series graph for {COIN} for the past {duration}."
        fig.update_layout(title=filename)
        img_bytes = fig.to_image(format="png")
        b = BytesIO(img_bytes)
    if DAYS == 7:
        duration = "7 days"
        filename = f"Time Series graph for {COIN} for the past {duration}."
        fig.update_layout(title=filename)
        img_bytes = fig.to_image(format="png")
        b = BytesIO(img_bytes)
    if DAYS == 30:
        duration = "month"
        filename = f"Time Series graph for {COIN} for the past {duration}."
        fig.update_layout(title=filename)
        img_bytes = fig.to_image(format="png")
        b = BytesIO(img_bytes)
    if DAYS == 182:
        duration = "6 months"
        filename = f"Time Series graph for {COIN} for the past {duration}."
        fig.update_layout(title=filename)
        img_bytes = fig.to_image(format="png")
        b = BytesIO(img_bytes)
    if DAYS == 365:
        duration = "1 year"
        filename = f"Time Series graph for {COIN} for the past {duration}."
        fig.update_layout(title=filename)
        img_bytes = fig.to_image(format="png")
        b = BytesIO(img_bytes)
    return b, filename



# Called whether there is a message in the chat
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('Hello'):
        await message.channel.send('Hi there, I am Crypbot the Crypto Currency Bot and I am at your service!')

    # send crypto price directly

    if message.content.lower() in db:
        query = cg.get_price(ids=message.content, vs_currencies='gbp', include_24hr_vol=True, include_24hr_change=True)
        price = query[message.content]['gbp']
        await message.channel.send(f'The current price of {message.content} is: £{price:,} (GBP)')

    # list all the available coins
    if message.content.startswith('$list'):
        await message.channel.send(db)

    # Check if a coin is supported
    if message.content.startswith('$support '):
        cryptoToBeChecked = message.content.split('$support ', 1)[1].lower()
        await message.channel.send(SupportedCrypto(cryptoToBeChecked))

    if message.content.startswith('$graph24hours'):
        cointobegraphed = message.content.split('$graph24hours ', 1)[1].lower()
        if cointobegraphed in db:
            b, filename = graphCrypto(COIN=cointobegraphed, DAYS=1)
            await message.channel.send(file=discord.File(b, filename=f"{filename}.png"))
        else:
            await message.channel.send(f"No information on {cointobegraphed.lower()} \n"
                                       f"Please try the following recognised cryptocurrencies: \n\n"
                                       f"{db}")

    if message.content.startswith('$graph1week'):
        cointobegraphed = message.content.split('$graph1week ', 1)[1].lower()
        if cointobegraphed in db:
            b, filename = graphCrypto(COIN=cointobegraphed, DAYS=7)
            await message.channel.send(file=discord.File(b, filename=f"{filename}.png"))
        else:
            await message.channel.send(f"No information on {cointobegraphed.lower()} \n"
                                       f"Please try the following recognised cryptocurrencies: \n\n"
                                       f"{db}")

    if message.content.startswith('$graph1month'):
        cointobegraphed = message.content.split('$graph1month ', 1)[1].lower()
        if cointobegraphed in db:
            b, filename = graphCrypto(COIN=cointobegraphed, DAYS=30)
            await message.channel.send(file=discord.File(b, filename=f"{filename}.png"))
        else:
            await message.channel.send(f"No information on {cointobegraphed.lower()} \n"
                                       f"Please try the following recognised cryptocurrencies: \n\n"
                                       f"{db}")

    if message.content.startswith('$graph6months'):
        cointobegraphed = message.content.split('$graph6months ', 1)[1].lower()
        if cointobegraphed in db:
            b, filename = graphCrypto(COIN=cointobegraphed, DAYS=182)
            await message.channel.send(file=discord.File(b, filename=f"{filename}.png"))
        else:
            await message.channel.send(f"No information on {cointobegraphed.lower()} \n"
                                       f"Please try the following recognised cryptocurrencies: \n\n"
                                       f"{db}")

    if message.content.startswith('$graph1year'):
        cointobegraphed = message.content.split('$graph1year ', 1)[1].lower()
        if cointobegraphed in db:
            b, filename = graphCrypto(COIN=cointobegraphed, DAYS=365)
            await message.channel.send(file=discord.File(b, filename=f"{filename}.png"))
        else:
            await message.channel.send(f"No information on {cointobegraphed.lower()} \n"
                                       f"Please try the following recognised cryptocurrencies: \n\n"
                                       f"{db}")

client.run(token)