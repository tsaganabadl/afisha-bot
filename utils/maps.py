# Обратный маппинг slug → человекочитаемое название
SLUG_TO_NAME = {
    "concert": "Концерт",
    "cinema": "Кино",
    "theater": "Театр",
    "exhibition": "Выставка",
    "master-class": "Мастер-класс",
    "sport": "Спорт",
    "entertainment": "Развлечения",
    "festival": "Фестиваль",
    "quest": "Квест",
}

def slug_to_name(slug: str) -> str:
    return SLUG_TO_NAME.get(slug, slug.capitalize() if slug else "Мероприятие")
