from RPLCD import i2c
from time import sleep
import requests, json
import datetime
from config import openWeatherAPI

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
  sleep(6)

def getWeatherData():
  global weatherData
  response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=42.956019&lon=-81.293685&appid=" + openWeatherAPI)
  weatherData = response.json()

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
  sleep(6)

while (True):
  # Update Data
  currentTime = datetime.datetime.now()
  elapsedTime = currentTime - lastUpdate
  elapsedTimeSeconds = elapsedTime.total_seconds()
  if (elapsedTimeSeconds > 60*10):
    lastUpdate = currentTime
    print("Updating Data")
    getWeatherData()

  displayTime()
  displayWeather()
  

