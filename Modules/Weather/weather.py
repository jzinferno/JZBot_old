from JZBot import dp, GetChatStatus, GetConfig, ReplyMsg, TextByLang
from httpx import AsyncClient

openweather_key = GetConfig('openweather_key')

def weather_text(text):
    return TextByLang({
        'ru': {
            'text_1': 'Погода в городе',
            'text_2': 'Температура',
            'text_3': 'Атмосферное давление',
            'text_4': 'Влажность воздуха',
            'text_5': 'Скорость ветра',
            'text_6': 'Город не найден',
            'text_7': 'Не удалось выполнить запрос',
        },
        'uk': {
            'text_1': 'Погода в місті',
            'text_2': 'Температура',
            'text_3': 'Атмосферний тиск',
            'text_4': 'Вологість повітря',
            'text_5': 'Швидкість вітру',
            'text_6': 'Місто не знайдено',
            'text_7': 'Не вдалося виконати запит',
        },
        'en': {
            'text_1': 'Weather in',
            'text_2': 'Temperature',
            'text_3': 'Atmosphere pressure',
            'text_4': 'Air humidity',
            'text_5': 'Wind speed',
            'text_6': 'City not found',
            'text_7': 'Failed to complete request',
        }
    }, text)

code_to_smile = {
    'Clear': '\U00002600',
    'Clouds': '\U00002601',
    'Rain': '\U00002614',
    'Drizzle': '\U00002614',
    'Thunderstorm': '\U000026A1',
    'Snow': '\U0001F328',
    'Mist': '\U0001F32B'
}

async def get_weather(citi):
    result = ''
    async with AsyncClient() as client:
        x = (await client.get('http://api.openweathermap.org/data/2.5/weather?appid=' + openweather_key + '&q=' + citi + '&units=metric&lang=en')).json()
        if x['cod'] != '404':
            result += f"{weather_text('text_1')}: {x['sys']['country']} {x['name']}\n"
            result += f"{weather_text('text_2')}: {x['main']['temp']}°C {code_to_smile[x['weather'][0]['main']]}\n"
            result += f"{weather_text('text_3')}: {x['main']['pressure']} мм рт. ст.\n"
            result += f"{weather_text('text_4')}: {x['main']['humidity']} [г/м³]\n"
            result += f"{weather_text('text_5')}: {x['wind']['speed']} м/с"
        else:
            result += weather_text('text_6')
    return result

@dp.message_handler(commands=['weather'])
async def main_weather(msg):
    if await GetChatStatus(msg) is not False:
        try:
            await ReplyMsg(msg, await get_weather(' '.join(msg.text.split()[1:])))
        except:
            await ReplyMsg(msg, weather_text('text_7'))
