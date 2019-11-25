import json
import requests



# Openweather API
def weather(city):
    payload = {'api_key': 'API_KEY_REMOVED'}

    appid = "0b8b9f1c9f93588e1ba7f35bf6dff48f"

    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city +"&appid="+appid

    res = requests.get(url,params=payload)
    res = res.json()
    pretty_data = json.dumps(res, indent=4)
    #print(pretty_data)
    description = res["weather"][0]["description"]
    #print("description:",description)
    temp = str(round(res["main"]["temp"] - 273.15,2))
    temp_min = str(round(res["main"]["temp_min"] - 273.15,2))
    temp_max = str(round(res["main"]["temp_max"] - 273.15,2))
    humidity = str(res["main"]["humidity"])

    message = "The weather in " + city + " is：" + description + ". The temperature now is: "+ \
              temp + "Cel, the highest temperature is: " + temp_max + "Cel, the lowest temperature is: "+ \
              temp_min + "Cel. The humidity is: " + humidity + "."

    return message
