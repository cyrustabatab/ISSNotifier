import requests,time
import os
from datetime import datetime
import smtplib
from twilio.reset import Client


my_email = 'calcguru2020@gmail.com'
to_email = 'ctabatab@gmail.com'

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN']

MY_LAT = 37.319309 # Your latitude
MY_LONG = -122.029259 # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.

def within_5_degrees():

    return (abs(MY_LAT) - iss_latitude <= 5) and (abs(MY_LONG - iss_longitude) <= 5)

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])


def is_night():
    time_now = datetime.now()
    return not sunrise <= time_now.hour <= sunset


while True:
    if within_5_degrees() and is_night():
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                             body="ISS is Overhead and its dark out. Look Up!",
                             from_='+15085065496',
                             to='+14084206801'
                         )

        print(message.status)
        '''
        with smtp.SMTP('smtp.gmail.com',port=587) as connection:
            connection.starttls()
            connection.login(user=email,password=os.environ.get('PASSWORD'))
            connection.sendmail(from_addr=my_email,to_addrs=to_email,msg="Subject: ISS OVERHEAD\n\nLOOK UP THE ISS IS OVERHEAD")
        '''
    time.wait(60)




#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



