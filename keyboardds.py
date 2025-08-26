from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
class WordCallback(CallbackData, prefix='word'):
    id: int

def words_keyboard_markup(words_list: list[dict]) -> InlineKeyboardMarkup:
    keyboard = []
    for i, word in enumerate(words_list):
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=word['name'],
                    callback_data=WordCallback(id=i).pack()
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)