import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from states import SearchStates
from config import CATEGORIES, DATE_FILTERS, PRICE_FILTERS, PAGE_SIZE
from keyboards.categories import categories_menu
from keyboards.dates import dates_menu, prices_menu, results_menu, empty_results_menu
from services.kudago_client import get_events
from services.formatter import format_events
from services import cache

router = Router()
logger = logging.getLogger(__name__)


async def safe_edit(message, text: str, **kwargs):
    """Безопасное редактирование — игнорирует 'message is not modified'."""
    try:
        await message.edit_text(text, **kwargs)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass  # ничего не делаем — контент идентичен
        else:
            raise


@router.callback_query(F.data == "menu_search")
async def start_search(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchStates.choosing_category)
    await safe_edit(
        callback.message,
        "🎯 *Шаг 1 из 3 — выбери категорию:*",
        reply_markup=categories_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()


# ---- Пресеты --------------------------------------------------------

@router.callback_query(F.data == "preset_free_today")
async def preset_free_today(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category="", category_name="Всё", date="today", price="free",
                            date_name="Сегодня", price_name="Бесплатные")
    await _show_results(callback, state, page=1)


@router.callback_query(F.data == "preset_cinema_tomorrow")
async def preset_cinema_tomorrow(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category="cinema", category_name="Кино", date="tomorrow", price="any",
                            date_name="Завтра", price_name="Любая")
    await _show_results(callback, state, page=1)


# ---- Шаг 1: категория ----------------------------------------------

@router.callback_query(F.data.startswith("cat:"))
async def category_chosen(callback: CallbackQuery, state: FSMContext):
    slug = callback.data.split(":", 1)[1]
    name = next((k for k, v in CATEGORIES.items() if v == slug), "Всё")
    await state.update_data(category=slug, category_name=name)
    await state.set_state(SearchStates.choosing_date)
    await safe_edit(
        callback.message,
        f"🏷 Категория: *{name}*\n\n📅 *Шаг 2 из 3 — выбери дату:*",
        reply_markup=dates_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()


# ---- Шаг 2: дата ---------------------------------------------------

@router.callback_query(F.data.startswith("date:"))
async def date_chosen(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split(":", 1)[1]
    name = next((k for k, v in DATE_FILTERS.items() if v == key), key)
    await state.update_data(date=key, date_name=name)
    await state.set_state(SearchStates.choosing_price)
    data = await state.get_data()
    await safe_edit(
        callback.message,
        f"🏷 {data['category_name']} • 📅 {name}\n\n"
        f"💰 *Шаг 3 из 3 — выбери цену:*",
        reply_markup=prices_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()


# ---- Шаг 3: цена ---------------------------------------------------

@router.callback_query(F.data.startswith("price:"))
async def price_chosen(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split(":", 1)[1]
    name = next((k for k, v in PRICE_FILTERS.items() if v == key), key)
    await state.update_data(price=key, price_name=name)
    await _show_results(callback, state, page=1)


# ---- Выдача результатов --------------------------------------------

async def _show_results(callback: CallbackQuery, state: FSMContext, page: int):
    data = await state.get_data()
    category = data.get("category", "")
    date = data.get("date", "today")
    price = data.get("price", "any")

    cache_key = f"{category}|{date}|{price}|{page}"
    cached = cache.get(cache_key)

    await callback.answer("Ищу мероприятия…")

    try:
        if cached:
            events, total = cached
        else:
            events, total = await get_events(category, date, price, page=page)
            cache.set(cache_key, (events, total))
    except Exception:
        logger.exception("Ошибка KudaGo")
        await safe_edit(
            callback.message,
            "⚠️ Не удалось получить данные от KudaGo.\n"
            "Попробуйте позже или измените фильтры.",
            reply_markup=empty_results_menu()
        )
        return

    if not events:
        await safe_edit(
            callback.message,
            "😕 По этим фильтрам ничего не нашлось.\n"
            "Попробуйте убрать цену или выбрать другую дату.",
            reply_markup=empty_results_menu()
        )
        await state.set_state(SearchStates.viewing_results)
        return

    start_index = (page - 1) * PAGE_SIZE + 1
    text = format_events(events, start_index=start_index)

    filters_line = (
        f"🏷 {data.get('category_name', 'Всё')} • "
        f"📅 {data.get('date_name', '')} • "
        f"💰 {data.get('price_name', '')}\n\n"
    )

    has_more = start_index + len(events) - 1 < total
    await state.update_data(page=page)
    await state.set_state(SearchStates.viewing_results)
    await safe_edit(
        callback.message,
        filters_line + text,
        reply_markup=results_menu(page=page, has_more=has_more),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )


# ---- Пагинация -----------------------------------------------------

@router.callback_query(F.data.startswith("more:"))
async def more_results(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split(":", 1)[1]) + 1
    await _show_results(callback, state, page=page)
