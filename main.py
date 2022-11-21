import requests
import datetime
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# "lat": 44.426765,
# "lon": 26.102537,

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {"https": os.environ["https_proxy"]}

account_sid = os.environ.get("TWI_ACC_SID")
auth_token = os.environ.get("TWI_AUT_TOK")


rain_codes = [1063, 1072, 1150, 1153, 1168, 1171, 1180, 1183, 1186, 1189, 1192, 1195, 1198, 1201, 1240, 1243, 1246, 1273, 1276]

parameters = {
    "q": "Bucharest",
    "days": 1,
    "key": "69df0465b29a49b796712442222111",
}

current_hour = int(str(datetime.datetime.now()).split(" ")[1].split(":")[0])

response_weather = requests.get("http://api.weatherapi.com/v1/forecast.json", params=parameters)
response_weather = requests.get("http://api.weatherapi.com/v1/forecast.json?q=Bucharest&days=1&key=69df0465b29a49b796712442222111")
response_weather.raise_for_status()

location_data = response_weather.json()["location"]
current_data = response_weather.json()["current"]
forecast_data = response_weather.json()["forecast"]["forecastday"][0]["hour"]

forecast_list = []

for hour in forecast_data:
    if hour["condition"]["code"] in rain_codes:
        forecast = {
            "time": int(hour["time"].split(" ")[1].split(":")[0]),
            "condition": hour["condition"]["text"],
            "temp": str(hour["temp_c"]) + " C",
        }

        forecast_list.append(forecast)

item = 0

client = Client(account_sid, auth_token, http_client=proxy_client)

will_rain = False

rain_hours = []


for entry in forecast_list:
    if current_hour <= forecast_list[item]["time"] <= (current_hour + 12):
        rain_times = {
            "time": forecast_list[item]['time'],
            "condition": forecast_list[item]['condition'],
            "temp": forecast_list[item]['temp'],
        }
        rain_hours.append(rain_times)

        will_rain = True
    item += 1

start_rain = rain_hours[0]["time"]
start_condition = rain_hours[0]["condition"]
start_temp = rain_hours[0]["temp"]

if will_rain is False:
    message = client.messages.create(
        body=f'It will rain in the next 12 hours, starting with {start_rain}, {start_condition} and there will be {start_temp}C',
        from_='+13466372476',
        to='FILL WITH PHONE NUMBER'
    )