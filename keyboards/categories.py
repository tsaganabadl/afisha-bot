from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CATEGORIES

def categories_menu():
    buttons, row = [], []
    for name, slug in CATEGORIES.items():
        row.append(InlineKeyboardButton(text=name, callback_data=f"cat:{slug}"))
        if len(row) == 2:
            buttons.append(row); row = []
    if row: buttons.append(row)
    buttons.append([InlineKeyboardButton(text="⬅️ В начало", callback_data="menu_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
