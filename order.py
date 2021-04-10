import logging
import time, sys, os
import api_data
import json
import time
import urllib
import requests
import base64
import hmac
import hashlib
import asyncio, signal, functools
import random

if 'win32' in sys.platform:
	# Windows specific event-loop policy & cmd
	asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


#===============================================================================
# env args
#===============================================================================
ENVARGS = []
if len(sys.argv) >= 1:
	for n in range(1,len(sys.argv)):
		ENVARGS.append(sys.argv[n])

#===============================================================================
# env args end
#===============================================================================


#===============================================================================
# logger setup
#===============================================================================
logger = logging.getLogger("binance-futures")
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
#===============================================================================
# logger setup end 
#===============================================================================

APIURLS = ["https://api.binance.com/","https://api1.binance.com/","https://api2.binance.com/","https://api3.binance.com/"]
URLv2 = "https://api.binance.com/"
API_KEY = api_data.binance['apiKey'] # put your API public key here.
API_SECRET = api_data.binance['secret'] # put your API private key here.
API_HEADER = {"X-MBX-APIKEY": API_KEY,}

SLEEP_INTERVAL = 0.15

def genNonce(): 
	# generates a nonce, used for authentication.
	return str(int(time.time() * 1000))

def payloadPacker(payload):
	payloadurl = urllib.parse.urlencode(payload)
	hashedsig = hmac.new(API_SECRET.encode('utf-8'), payloadurl.encode('utf-8'), hashlib.sha256).hexdigest()
	payload.update({"signature":hashedsig})
	return payload


def place_buy_order(**kwargs):
		payload = {
			"timestamp":genNonce(),
			"symbol":kwargs['symbol'],
			"side":kwargs['side'],
			"quantity":kwargs['quantity'],
			"price":kwargs['price'],
			"type":kwargs["type"],
			"timeInForce":kwargs['timeInForce'],
		}
		
		payload = payloadPacker(payload)
		r = requests.post(random.choice(APIURLS) + "api/v3/order", headers=API_HEADER, params=payload, verify=True,timeout=5)
		return r

def balances(): # see your balances.
	payload = {
		"timestamp":genNonce(),
	}
	
	payload = payloadPacker(payload)
	r = requests.get(URLv2 + "api/v3/account", headers=API_HEADER, params=payload, verify=True,timeout=5)
	
	print( r.json())
	return r


def assetQuantityPrecision(symbol,value=2):
	for s in exchange_info["symbols"]:
		if s["symbol"] == symbol:
			value = s["quantityPrecision"]
			break

	return value

def assetPricePrecision(symbol,value=2):
	for s in exchange_info["symbols"]:
		if s["symbol"] == symbol:
			value = s["pricePrecision"]
			# print(symbol,value)
			break
	return value


if len(ENVARGS) < 3:
	logger.info("please provide 3 parameters in order: symbolname amount price")
	logger.info("to sell 100 TLM at $4: TLMUSDT -100 4")
	logger.info("to buy 50 TLM at $2: TLMUSDT 50 2")
	quit()



logger.info("using binance API credentials")



async def launchpadorders():
	while True:
		try:
			symbol = ENVARGS[0].upper()
			side = "BUY" if float(ENVARGS[1])> 0 else "SELL"
			amount = abs(float(ENVARGS[1]))
			price = float(ENVARGS[2])
			logger.info("Trying to execute orders: %s %s %s @ $%s" % (side,amount,symbol,price))
			order = {
			"symbol":symbol,
			"side":side,
			"quantity":"{0:.8f}".format(amount),
			"price":"{0:.8f}".format(price),
			"type":"LIMIT",
			"timeInForce":"GTC"
			}

			executeorder = place_buy_order(**order).json()
			if "code" in executeorder.keys():
				logger.info("%s",executeorder["msg"])
			else:
				logger.info("Success, return data: %s \n",executeorder)
				loop.stop()
		except:
			e = sys.exc_info()
			logger.error("EXCEPTION ERROR - line %s, %s %s" % (e[-1].tb_lineno, type(e).__name__, e))
		finally:
			delay = await asyncio.sleep(SLEEP_INTERVAL)




#===============================================================================
# loop signal handler to exit with ctrl+c
#===============================================================================
def ask_exit(signame):
	logger.info("Got signal %s: exiting" % signame)
	loop.stop()


loop = asyncio.get_event_loop()
for signame in ('SIGINT', 'SIGTERM'):
	try:
		loop.add_signal_handler(getattr(signal, signame),functools.partial(ask_exit, signame))
	except NotImplementedError:
   		pass  # Ignore if not implemented. Means this program is running in windows.


#===============================================================================
# end of loop signal handler
#===============================================================================




def run_limitorders():
	
	asyncio.ensure_future(launchpadorders())  
	
	
	# asyncio.ensure_future(backupdata()) 
	
	print("Event loop running forever, press Ctrl+C to interrupt.")
	print("pid %s: send SIGINT or SIGTERM to exit." % os.getpid())
	
	try:
		loop.run_forever()
	finally:
		loop.close()


if __name__ == '__main__':
	run_limitorders()



