from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START_COMMAND = Command("start")
WEATHER_OF_CITY = Command("weather_of_city")

START_BOT_COMMAND = BotCommand(command="start", description="Start")
WEATHER_BOT_OF_CITY_COMMAND = BotCommand(command="weather_of_city", description="Впишіть нзаву міста й дізнайтесь там погоду в тому місті")