import requests
import config
import translate


api_key = open('api_key.txt', 'r').read()
result = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={config.LOCATION}'
                      f'&units=metric&appid={api_key}')

translator = translate.Translator(to_lang="ru")

description = result.json()['weather'][0]['description']
description_ru = translator.translate(description)

temperature = round(result.json()['main']['temp'])
feels_like = round(result.json()['main']['feels_like'])
temp_max = round(result.json()['main']['temp_max'])
temp_min = round(result.json()['main']['temp_min'])


def get_weather() -> str:
    message = f"{temperature}°C, {description_ru}"
    message += ". не забудь зонт\n" if "rain" in description else "\n"
    message += f"температура от {temp_min}°C до {temp_max}°C. ощущается как {feels_like}°C"
    message += ". одевайся теплее" if feels_like <= -10 else ""
    return message
