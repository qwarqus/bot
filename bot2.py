import asyncio
import logging
import sys
import random as r
import json
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from conf2 import BOT_TOKEN
from keyboardds import words_keyboard_markup, WordCallback

# Bot token can be obtained via https://t.me/BotFather
TOKEN = BOT_TOKEN

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"привіт, {html.bold(message.from_user.full_name)}!")


def get_words(file_path: str = 'data2.json', word_id: int | None = None):
    with open(file_path, 'r', encoding='utf-8') as fp:
        words = json.load(fp)
        if word_id != None and word_id < len(words):
            return words[word_id]
        return words


@dp.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    await message.answer(f"Привіт це бот крокодил, тобі треба відгадати слово яке загадав бот.")


@dp.message(StartGame)
async def command_StartGame_handler(message: Message) -> None:
    words = get_words()
    r.choice(words)
    markup = words_keyboard_markup(word_list=data)
    await message.answer(f"Почнемо гру,\n"
                         f"Підсказка до слова {r_w['helpa']}",
                         reply_markup=markup)


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
