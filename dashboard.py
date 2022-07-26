from RPLCD import i2c
from time import sleep
import requests, json
import datetime
from config import openWeatherAPI, alphavantageAPI

# Set up LCD Display
cols = 20
rows = 4
charmap = 'A00'
i2c_expander = 'PCF8574'
address = 0x27
port = 1
lcd = i2c.CharLCD(i2c_expander=i2c_expander, address=address, port=port, charmap=charmap, cols=cols, rows=rows)

# API Call Globals
lastUpdate = datetime.datetime(2000, 1, 1)
weatherData = {}
btc_usd = 0
eth_usd = 0
spy_data = {}

def displayWeather():
  global weatherData
  if weatherData["cod"] != "404":
    current_temperature = weatherData["main"]["temp"] - 273.15
    feels_like = weatherData["main"]["feels_like"] - 273.15
    weather_desc = weatherData["weather"][0]["description"]
    lcd.clear()
    lcd.write_string('----TEMPERATURE-----')
    lcd.write_string('    Now: ' + str(current_temperature) + 'C')
    lcd.cursor_pos = (2, 0)
    lcd.write_string(' Feels Like: ' + str(feels_like) + 'C')
    lcd.cursor_pos = (3, 0)
    lcd.write_string(weather_desc.title().center(20))
    lcd.crlf()
  else:
    lcd.clear()
    lcd.write_string('-------WEATHER------')
    lcd.write_string('ERROR: No data')
    lcd.crlf()

def getWeatherData():
  global weatherData
  response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=42.956019&lon=-81.293685&appid=" + openWeatherAPI)
  weatherData = response.json()

def getCryptoData():
  global btc_usd
  global eth_usd
  url_btc_usd = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey=' + alphavantageAPI
  r_btc_usd = requests.get(url_btc_usd)
  data_btc_usd = r_btc_usd.json()
  btc_usd = data_btc_usd["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
  url_eth_usd = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=ETH&to_currency=USD&apikey=' + alphavantageAPI
  r_eth_usd = requests.get(url_eth_usd)
  data_eth_usd = r_eth_usd.json()
  eth_usd = data_eth_usd["Realtime Currency Exchange Rate"]["5. Exchange Rate"]

def getStocksData():
  global spy_data
  url_spy = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=SPY&apikey=' + alphavantageAPI
  r_spy = requests.get(url_spy)
  spy_data = r_spy.json()

def displayStocksData():
  global spy_data
  spy_string = 'SPY: $' +  str(round(float(spy_data["Global Quote"]["05. price"]),2)) + ' ' + str(round(float(spy_data["Global Quote"]["10. change percent"][:-1]),2)) + '%'
  lcd.clear()
  lcd.write_string('-------STOCKS-------')
  lcd.cursor_pos = (1, 0)
  lcd.write_string("EOD:".center(20))
  lcd.cursor_pos = (2, 0)
  lcd.write_string(spy_string.center(20))
  lcd.crlf()

def displayCryptoData():
  global btc_usd
  global eth_usd
  eth_string = 'ETH/USD: $' + str(int(float(eth_usd)))
  btc_string = 'BTC/USD: $' + str(int(float(btc_usd)))
  lcd.clear()
  lcd.write_string('-------CRYPTO-------')
  lcd.write_string(eth_string.center(20))
  lcd.cursor_pos = (2, 0)
  lcd.write_string(btc_string.center(20))
  lcd.crlf()


def displayTime():
  currentTime = datetime.datetime.now()
  displayTime = currentTime.strftime('       %I:%M')
  displayDate = currentTime.strftime(' %a, %b %d, %Y')
  lcd.clear()
  lcd.write_string('--------TIME--------')
  lcd.write_string(displayTime)
  lcd.cursor_pos = (3, 0)
  lcd.write_string(displayDate)
  lcd.crlf()

while (True):
  # Update Data
  currentTime = datetime.datetime.now()
  elapsedTime = currentTime - lastUpdate
  elapsedTimeSeconds = elapsedTime.total_seconds()
  if (elapsedTimeSeconds > 60*12):
    lastUpdate = currentTime
    print("Updating Data")
    getWeatherData()
    getCryptoData()
    getStocksData()

  displayTime()
  sleep(6)
  displayWeather()
  sleep(6)
  displayCryptoData()
  sleep(6)
  print(currentTime.weekday())
  print(currentTime.hour)
  if (currentTime.hour >= 16 and currentTime.weekday() != 5 and currentTime.weekday() != 6):
    displayStocksData()
    sleep(6)
  
