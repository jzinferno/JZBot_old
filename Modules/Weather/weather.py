from JZBot import dp, GetChatStatus, GetConfig, ReplyMsg, TextByLang, Message
from httpx import AsyncClient

openweather_key = GetConfig('openweather_key')

def weather_text(number):
    return TextByLang({
        'ru': [
            'Погода в городе',
            'Температура',
            'Атмосферное давление',
            'Влажность воздуха',
            'Скорость ветра',
            'Город не найден',
            'Не удалось выполнить запрос'
        ],
        'uk': [
            'Погода в місті',
            'Температура',
            'Атмосферний тиск',
            'Вологість повітря',
            'Швидкість вітру',
            'Місто не знайдено',
            'Не вдалося виконати запит'
        ],
        'en': [
            'Weather in',
            'Temperature',
            'Atmosphere pressure',
            'Air humidity',
            'Wind speed',
            'City not found',
            'Failed to complete request'
        ]
    }, number)

code_to_smile = {
    'Clear': '\U00002600',
    'Clouds': '\U00002601',
    'Rain': '\U00002614',
    'Drizzle': '\U00002614',
    'Thunderstorm': '\U000026A1',
    'Snow': '\U0001F328',
    'Mist': '\U0001F32B'
}

async def get_weather(city):
    result = ''
    async with AsyncClient() as client:
        x = (await client.get('http://api.openweathermap.org/data/2.5/weather?appid=' + openweather_key + '&q=' + city + '&units=metric&lang=en')).json()
        if x['cod'] != '404':
            result += f"{weather_text(0)}: {x['sys']['country']} {x['name']}\n"
            result += f"{weather_text(1)}: {x['main']['temp']}°C {code_to_smile[x['weather'][0]['main']]}\n"
            result += f"{weather_text(2)}: {x['main']['pressure']} мм рт. ст.\n"
            result += f"{weather_text(3)}: {x['main']['humidity']} [г/м³]\n"
            result += f"{weather_text(4)}: {x['wind']['speed']} м/с"
        else:
            result += weather_text(5)
    return result

@dp.message_handler(commands=['weather'])
async def main_weather(msg: Message):
    if await GetChatStatus(msg) is not False:
        try:
            await ReplyMsg(msg, await get_weather(' '.join(msg.text.split()[1:])))
        except:
            await ReplyMsg(msg, weather_text(6))
