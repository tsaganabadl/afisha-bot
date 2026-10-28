import asyncio
import logging
import re
from datetime import datetime, timedelta
import aiohttp

from config import KUDA_API, CITY_SLUG, PAGE_SIZE

logger = logging.getLogger(__name__)

def _date_range(filter_key: str):
    now = datetime.now()
    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)

    if filter_key == "today":
        return int(start_of_today.timestamp()), int((start_of_today + timedelta(days=1)).timestamp())
    if filter_key == "tomorrow":
        tmr = start_of_today + timedelta(days=1)
        return int(tmr.timestamp()), int((tmr + timedelta(days=1)).timestamp())
    if filter_key == "weekend":
        days_until_sat = (5 - now.weekday()) % 7
        sat = start_of_today + timedelta(days=days_until_sat)
        sun_end = sat + timedelta(days=2)
        return int(sat.timestamp()), int(sun_end.timestamp())
    return None, None

async def get_events(category_slug: str, date_filter: str, price_filter: str, page: int = 1):
    date_from, date_to = _date_range(date_filter)

    params = {
        "location": CITY_SLUG,
        "page": page,
        "page_size": PAGE_SIZE,
        "expand": "place",
        "text_format": "plain",
        "fields": "id,title,dates,place,price,categories,site_url",
    }
    if category_slug:
        params["categories"] = category_slug
    if date_from and date_to:
        params["actual_since"] = date_from
        params["actual_until"] = date_to
    if price_filter == "free":
        params["is_free"] = "true"

    last_error = None
    for attempt in range(3):
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(KUDA_API, params=params) as resp:
                    if resp.status != 200:
                        last_error = f"HTTP {resp.status}"
                        logger.warning("KudaGo attempt %s: %s", attempt + 1, last_error)
                        await asyncio.sleep(1)
                        continue
                    data = await resp.json()
                    events = data.get("results", [])
                    events = _filter_by_price(events, price_filter)
                    return events, data.get("count", 0)
        except Exception as e:
            last_error = str(e)
            logger.warning("KudaGo attempt %s error: %s", attempt + 1, last_error)
            await asyncio.sleep(1)

    logger.error("KudaGo failed after 3 attempts: %s", last_error)
    raise RuntimeError(f"KudaGo недоступен: {last_error}")

def _filter_by_price(events, price_filter):
    if price_filter not in ("under_1000", "under_3000"):
        return events
    limit = 1000 if price_filter == "under_1000" else 3000
    result = []
    for e in events:
        price_text = (e.get("price") or "").lower()
        if "бесплат" in price_text or price_text == "":
            result.append(e)
            continue
        nums = [int(n) for n in re.findall(r"\d+", price_text.replace(" ", ""))]
        if nums and min(nums) <= limit:
            result.append(e)
    return result
