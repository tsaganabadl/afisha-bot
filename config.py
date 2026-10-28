import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# KudaGo API
KUDA_API = "https://kudago.com/public-api/v1.4/events/"

# Город фиксирован — Москва (по ТЗ, раздел 10)
CITY_SLUG = "msk"
CITY_NAME = "Москва"

# Категории: название → slug в KudaGo (раздел 8.1)
# «Развлечения» — составная категория, склеиваем несколько slug через запятую
CATEGORIES = {
    "Концерт": "concert",
    "Кино": "cinema",
    "Театр": "theater",
    "Выставка": "exhibition",
    "Мастер-класс": "master-class",
    "Спорт": "sport",
    "Развлечения": "entertainment,festival,quest",
    "Показать всё": "",
}

# Фильтры по цене (раздел 4, сценарий 2)
PRICE_FILTERS = {
    "Бесплатные": "free",
    "До 1000 ₽": "under_1000",
    "До 3000 ₽": "under_3000",
    "Любая": "any",
}

# Фильтры по дате (раздел 4, сценарий 2)
DATE_FILTERS = {
    "Сегодня": "today",
    "Завтра": "tomorrow",
    "Выходные": "weekend",
}

PAGE_SIZE = 10
