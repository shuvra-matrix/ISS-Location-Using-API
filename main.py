import time
import requests
from datetime import datetime
import smtplib

my_email = "" #YOUR EMAIL
my_password = "" #YOUR PASSWORD


def day_time():
    my_location = {"lat": 23.647970, "lng": 88.128418, "formatted": 0}
    request = requests.get(url="https://api.sunrise-sunset.org/json", params=my_location)
    request.raise_for_status()
    data = request.json()
    sunrise_time = data["results"]["sunrise"]
    sunset_time = data["results"]["sunset"]
    sunrise_hours = int(sunrise_time.split("T")[1].split(":")[0])
    sunset_hours = int(sunset_time.split("T")[1].split(":")[0])
    time_now = datetime.now()
    hour_now = time_now.hour
    if sunset_hours < hour_now < sunrise_hours:
        return True


def iss_location():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])
    my_latitude = 23.647970
    my_longitude = 88.128418
    if my_latitude-5 <= latitude <= my_latitude+5 and my_longitude-5 <= longitude <= my_longitude+5:
        return True


while True:
    time.sleep(60)
    if iss_location() and day_time():
        with smtplib.SMTP("smtp.gmail.com", port=587) as email:
            email.starttls()
            email.login(user=my_email, password=my_password)
            email.sendmail(from_addr=my_email, to_addrs="shuvra232@gmail.com",
                           msg=f"Subject:ISS Location\n\nISS is in your location now ! Look At")
