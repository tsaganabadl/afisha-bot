from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import DATE_FILTERS, PRICE_FILTERS

def dates_menu():
    buttons = [[InlineKeyboardButton(text=name, callback_data=f"date:{key}")]
               for name, key in DATE_FILTERS.items()]
    buttons.append([InlineKeyboardButton(text="⬅️ В начало", callback_data="menu_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def prices_menu():
    buttons = [[InlineKeyboardButton(text=name, callback_data=f"price:{key}")]
               for name, key in PRICE_FILTERS.items()]
    buttons.append([InlineKeyboardButton(text="⬅️ В начало", callback_data="menu_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def results_menu(page: int, has_more: bool):
    buttons = []
    if has_more:
        buttons.append([InlineKeyboardButton(text="➡️ Показать ещё", callback_data=f"more:{page}")])
    buttons.append([InlineKeyboardButton(text="🏠 В начало", callback_data="menu_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def empty_results_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Изменить фильтры", callback_data="menu_search")],
        [InlineKeyboardButton(text="🏠 В начало", callback_data="menu_back")],
    ])
