from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from keyboards.main import main_menu

router = Router()

WELCOME = (
    "👋 Привет! Я бот *«Афиша»*.\n\n"
    "Помогу подобрать досуг в Москве: концерты, кино, театр, "
    "выставки, мастер-классы, спорт и развлечения.\n\n"
    "Выбери действие:"
)

ABOUT = (
    "ℹ️ *О боте*\n\n"
    "Бот подбирает мероприятия в Москве по категории, дате и цене.\n\n"
    "*Источник данных:* KudaGo Public API v1.4 "
    "(открытый, без ключа доступа).\n\n"
    "*Ограничения:*\n"
    "• Город — только Москва.\n"
    "• Данные обновляются на стороне KudaGo.\n"
    "• Не все события Москвы есть в базе KudaGo.\n"
    "• Ссылки ведут на внешний сайт KudaGo."
)

HELP = (
    "❓ *Помощь*\n\n"
    "*Как пользоваться:*\n"
    "1. Нажми «Подобрать мероприятие».\n"
    "2. Выбери категорию.\n"
    "3. Выбери дату.\n"
    "4. Выбери цену.\n"
    "5. Смотри карточки и жми «Показать ещё».\n\n"
    "*Команды:*\n"
    "/start — главное меню\n"
    "/help — эта справка\n"
    "/about — о боте"
)


async def safe_edit(message, text: str, **kwargs):
    try:
        await message.edit_text(text, **kwargs)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(WELCOME, reply_markup=main_menu(), parse_mode="Markdown")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP, parse_mode="Markdown")


@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(ABOUT, parse_mode="Markdown")


@router.callback_query(F.data == "menu_back")
async def back_to_menu(callback: CallbackQuery, state):
    await state.clear()
    await safe_edit(
        callback.message,
        WELCOME,
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "menu_about")
async def menu_about(callback: CallbackQuery):
    await safe_edit(
        callback.message,
        ABOUT,
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "menu_help")
async def menu_help(callback: CallbackQuery):
    await safe_edit(
        callback.message,
        HELP,
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()
