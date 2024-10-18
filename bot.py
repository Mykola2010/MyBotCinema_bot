import aiohttp
import asyncio
import logging
import sys
from config import BOT_TOKEN as TOKEN
from config import API_KEY
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from commands import WEATHER_OF_CITY, WEATHER_BOT_OF_CITY_COMMAND

dp = Dispatcher()


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

weather_type = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Хмарно \U00002601",
    "Rain": "Дощ \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Сніг \U0001F328",
    "Mist": "Туман \U0001F32B"
}


@dp.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.answer(
        f"Добрий день {html.bold(message.from_user.full_name)}, я бот, який говорить про погоду в місті!")


@dp.message(WEATHER_OF_CITY)
async def get_weather_city(message: Message) -> None:
    await message.answer("Напиши мені назву міста латиницею, і я надішлю тобі прогноз погоди!")


@dp.message()
async def get_weather_weather(message: Message) -> None:
    city_name = message.text.strip()
    logging.info(f"Запит погоди для міста: {city_name}")

    try:
        async with aiohttp.ClientSession() as session: #відкриває сесію для HTTP-запитів.
            async with session.get(
                    f"http://api.openweathermap.org/data/2.5/weather?q={city_name.lower()}&appid={API_KEY}&units=metric") as response:

                logging.info(f"Отримано відповідь з OpenWeather API. Статус код: {response.status}")

                if response.status == 200:
                    data = await response.json()

                    logging.info(f"Дані з OpenWeather API: {data}")

                    if "main" in data and "weather" in data:
                        city = data["name"]
                        cur_weather = data["main"]["temp"]
                        weather_description = data["weather"][0]["main"]

                        wd = weather_type.get(weather_description, "Подивіться у вікно, щоб дізнатися погоду!")

                        humidity = data["main"]["humidity"]
                        pressure = data["main"]["pressure"]
                        wind = data["wind"]["speed"]
                        feels_like = data["main"]["feels_like"]
                        sunrise_timestamp = data["sys"]["sunrise"]
                        sunset_timestamp = data["sys"]["sunset"]
                        country = data["sys"]["country"]
                        length_of_the_day = (sunset_timestamp - sunrise_timestamp) // 60

                        await message.reply(f"***Погода у місті: {city}***\n"
                                            f"Температура: {round(cur_weather)}°C {wd}\n"
                                            f"Відчувається як: {round(feels_like)}°C\n"
                                            f"Вологість: {humidity}%\n"
                                            f"Тиск: {pressure} мм.рт.ст\n"
                                            f"Вітер: {wind} м/с\n"
                                            f"Тривалість дня: {length_of_the_day} хв\n"
                                            f"Країна: {country}\n"
                                            f"***Гарного дня!***")
                    else:
                        logging.error(f"Відсутні ключі 'main' або 'weather' у відповіді: {data}")
                        await message.answer("🙄 Перевірте назву міста 🙄")
                else:
                    logging.error(f"Статус код помилки: {response.status}")
                    await message.answer(f"Виникла помилка при отриманні погоди: статус код {response.status}")

    except Exception as exception:
        logging.error(f"Помилка при отриманні погоди: {exception}")
        await message.answer("Виникла помилка при отриманні погоди")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands([WEATHER_BOT_OF_CITY_COMMAND])

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())