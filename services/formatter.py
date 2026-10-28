from datetime import datetime
from utils.maps import slug_to_name
import time

def _fmt_date(ts):
    try:
        return datetime.fromtimestamp(int(ts)).strftime("%d.%m.%Y %H:%M")
    except Exception:
        return "дата уточняется"

def _pick_actual_date(dates):
    """Возвращает ближайшую будущую дату (start) из списка dates."""
    if not dates:
        return None
    now = time.time()
    candidates = []
    for d in dates:
        start = d.get("start")
        if start and start > 0:  # отсекаем «до нашей эры»
            if start >= now:
                candidates.append(start)
    if candidates:
        return min(candidates)
    # если будущих нет — берем последнюю положительную
    positives = [d["start"] for d in dates if d.get("start", 0) > 0]
    return max(positives) if positives else None

def format_events(events, start_index=1):
    if not events:
        return ""

    blocks = []
    for i, e in enumerate(events, start=start_index):
        title = e.get("title", "Без названия")

        cats = e.get("categories") or []
        cat = slug_to_name(cats[0]) if cats else "Мероприятие"

        place = e.get("place") or {}
        place_title = place.get("title") or "Место не указано"
        address = place.get("address") or ""

        dates = e.get("dates") or []
        actual_start = _pick_actual_date(dates)
        date_str = _fmt_date(actual_start) if actual_start else "дата уточняется"

        price = e.get("price") or "Уточняйте"
        url = e.get("site_url") or "https://kudago.com/msk/"

        block = (
            f"{i}. *{title}*\n"
            f"🏷 {cat}\n"
            f"📍 {place_title}"
        )
        if address:
            block += f"\n🏠 {address}"
        block += f"\n📅 {date_str}\n💰 {price}\n[Подробнее]({url})"
        blocks.append(block)

    header = "🎫 *Найденные мероприятия:*\n\n"
    return header + "\n\n".join(blocks)
