import asyncio
import logging
import sys
import json
import cohere

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, URLInputFile, ReplyKeyboardRemove
from models import Book
from conf import BOT_TOKEN, ADMIN_ID
from commands import (START_BOT_COMMAND, BOOKS_BOT_COMMAND, BOOKS_CREATED_COMMAND,
                       BOOKS_COMMAND, BOOKS_BOT_CREATE_COMMAND)
from keyboards import books_keyboard_markup, BookCallback
from state import BookForm

TOKEN = BOT_TOKEN
dp = Dispatcher()


@dp.message(Command('/pop'))
async def info(message: Message) -> None:
    await message.answer(f'hello {message.from_user.id}')


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    logging.info(f'{message.from_user.full_name} has started')


def get_books(file_path: str = 'data.json', book_id: int | None = None):
    with open(file_path, 'r', encoding='utf-8') as fp:
        books = json.load(fp)
        if book_id is not None and book_id < len(books):
            return books[book_id]
        return books


def add_books(book: dict, file_path: str = 'data.json'):
    books = get_books()
    if books:
        books.append(book)
        with open(file_path, 'w', encoding='utf-8') as fp:
            json.dump(
                books,
                fp,
                indent=4,
                ensure_ascii=False
            )


@dp.message(BOOKS_COMMAND)
async def books(message: Message) -> None:
    data = get_books()
    markup = books_keyboard_markup(book_list=data)
    await message.answer("Список книг. Нажміть на кнопку", reply_markup=markup)


@dp.callback_query(BookCallback.filter())
async def callback_book(callback: CallbackQuery, callback_data: BookCallback) -> None:
    book_id = callback_data.id
    book_data = get_books(book_id=book_id)
    book = Book(**book_data)

    text = (
        f"Книга: {book.name}\n"
        f"Опис: {book.description}\n"
        f"Рейтинг: {book.rating}\n"
        f"Жанр: {book.genre}\n"
        f"Автори: {', '.join(book.authors)}\n"
    )

    try:
        await callback.message.answer_photo(
            caption=text,
            photo=URLInputFile(
                book.poster,
                filename=f"{book.name}_cover.{book.poster.split('.')[-1]}"
            )
        )
    except Exception as e:
        await callback.message.answer(text)
        logging.error(f"Failed to load images for book {book.name}: {str(e)}")


@dp.message(BOOKS_CREATED_COMMAND)
async def book_create(message: Message, state: FSMContext) -> None:
    if message.from_user.id == int(ADMIN_ID):
        await state.set_state(BookForm.name)
        await message.answer("Введіть назву книги", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("тільки для адміна", reply_markup=ReplyKeyboardRemove())


@dp.message(BookForm.name)
async def book_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(BookForm.description)
    await message.answer("Введіть опис", reply_markup=ReplyKeyboardRemove())


@dp.message(BookForm.description)
async def description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(BookForm.rating)
    await message.answer("Введіть рейтинг книги", reply_markup=ReplyKeyboardRemove())


@dp.message(BookForm.rating)
async def rating(message: Message, state: FSMContext) -> None:
    await state.update_data(rating=message.text)
    await state.set_state(BookForm.genre)
    await message.answer("Введіть жанр книги", reply_markup=ReplyKeyboardRemove())


@dp.message(BookForm.genre)
async def genre(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text)
    await state.set_state(BookForm.authors)
    await message.answer("Введіть авторів (через кому)", reply_markup=ReplyKeyboardRemove())


@dp.message(BookForm.authors)
async def book_authors(message: Message, state: FSMContext) -> None:
    authors = [x.strip() for x in message.text.split(",")]
    await state.update_data(authors=authors)
    await state.set_state(BookForm.poster)
    await message.answer("Введіть посилання на обкладинку книги.", reply_markup=ReplyKeyboardRemove())


@dp.message(BookForm.poster)
async def book_poster(message: Message, state: FSMContext) -> None:
    await state.update_data(poster=message.text)
    data = await state.get_data()

    book = Book(**data)
    add_books(book.dict())

    await state.clear()
    await message.answer(f"Книгу «{book.name}» успішно додано", reply_markup=ReplyKeyboardRemove())


def generate_text(prompt: str):
    co = cohere.ClientV2(api_key="Ualsm3uh6PTjQfLNiwzqIwS48urgKfPA0cwSfiZT")

    res = co.chat(
        model="command-a-03-2025",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return res.message.content[0].text


@dp.message()
async def echo_handler(message: Message) -> None:
    user_input = message.text
    await message.answer(f'{message.from_user.full_name}, зачекай... відповідь генерується...')
    generated_text = generate_text(user_input)
    await message.answer(generated_text)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands(
        [
            START_BOT_COMMAND,
            BOOKS_BOT_COMMAND,
            BOOKS_BOT_CREATE_COMMAND
        ]
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
