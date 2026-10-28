from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Подобрать мероприятие", callback_data="menu_search")],
        [InlineKeyboardButton(text="🆓 Бесплатно сегодня", callback_data="preset_free_today")],
        [InlineKeyboardButton(text="🎬 В кино завтра", callback_data="preset_cinema_tomorrow")],
        [
            InlineKeyboardButton(text="ℹ️ О боте", callback_data="menu_about"),
            InlineKeyboardButton(text="❓ Помощь", callback_data="menu_help"),
        ],
    ])
