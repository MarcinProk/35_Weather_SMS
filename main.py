import requests
from twilio.rest import Client

API_KEY = 'your_api_key'
auth_token = 'your_auth_token'
account_SID = 'your_acc_sid'


# ------------------------------------- WEATHER API ----------------------------------- #
# PROGRAM CODZIENNIE WYSYŁA SMS Z INFORMACJĄ O TEMPERATURZE ORAZ OPADACH
MY_LAT = 51.141390
MY_LNG = 17.027440

twilio_nr = "+12677280535"
to_phone_number = "+48 536321186"

parameters = {
    "lat": MY_LAT,
    "lon": MY_LNG,
    "appid": API_KEY,
    "units": "metric",
    "cnt": 4,                # 4 dane, czyli 4 x 3 godziny, prognoza na 12 godzin
    "lang": "pl"
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
# print(response.status_code)
response.raise_for_status()
data = response.json()

temperature_feels = data["list"][0]["main"]["feels_like"]
# print(temperature_feels)
weather_id = data["list"][0]["weather"][0]["id"]
# print(weather_id)
weather_description = data["list"][0]["weather"][0]["description"]
# print(weather_description)

# weather_id code list for next 12 hour
will_rain = False
for hour_data in data["list"]:
    weather_id = hour_data["weather"][0]["id"]          # iteruję przez hour_data (tutaj 0,1,2,3), więc zamiast tego podstawiać się będzie ten indeks
    if int(weather_id) < 700:
        will_rain = True
if will_rain:
    client = Client(account_SID, auth_token)
    message = client.messages.create(
        body = f"Cześć! Dziś odczuwalna temperatura to ok {temperature_feels}°C. Będzie dziś padać, zabierz parasol ☂️.",
        from_ = twilio_nr,
        to = to_phone_number
    )
else:
    client = Client(account_SID, auth_token)
    message = client.messages.create(
        body = f"Cześć! Dziś odczuwalna temperatura to ok {temperature_feels}°C. Nie będzie dziś padać!",
        from_ = twilio_nr,
        to = to_phone_number
    )
print(message.status)