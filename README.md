# binance_launch_order
This python script will place your limit buy or sell order when a new market is listed.<br>
It will keep trying (loop) several times a second until the market is active.
It also can be used to place limit orders from command line.

# Install intructions:

requires Python 3+ and the following additional modules:<br/>

requests<br/>

If you are starting with a fresh python v3.X install, make sure to run "pip install requests" and "pip install rich"  to get your python environment set up to run everything that this script asks for. If your default python install is another version (2.7), you might need to use a virtual environment like Conda (https://docs.conda.io/en/latest/miniconda.html)
<br>
rename api_data_template.py to api_data.py and add you ftx API key/secret inside the file.

# Running the script:
python order.py SYMBOL AMOUNT PRICE<br/>
Negative amounts are sales, positive amounts are buys.<br/><br/>

example to sell 1 BTC at $50000:<br/>
python order.py btcusdt -1 50000<br/><br/>

example to buy 10 BNB at $350:<br/>
python order.py bnbusdt 10 350<br/>

Be careful, it doesn't do ANY verifications, if you type price too low when selling or too high when buying, the order will execute at market price. Errors will be show on the log.

The script will keep running forever until completion of a single order or canceled (press CTRL+C/CMD+C)

If you like this and made a lot of extra money, feel free to contribute to my beer fund<br/>
btc: 1DN6jvGZbQkYT9RoCjCVzTs5MwC3xvdmMh<br/>
ltc: LTT8Gj8nnwBCEGAcapjfLy9EyZtiu6Ntqh<br/>
usdt TRC20: TYXR6fkC3dKwfSFtEdkgcPVr2em3cPUnT9<br/>
bnb bsc: 0x8d291FD4413C947559E89F78534400ccaB9BDe92<br>

# Help? Bugs?
https://molibden.io/about/
