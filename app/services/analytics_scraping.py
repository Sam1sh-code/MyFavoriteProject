import matplotlib
matplotlib.use('Agg') # Фикс: запрещаем Matplotlib пытаться открыть окно на сервере
import matplotlib.pyplot as plt
import requests
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import time
import os

templates = Jinja2Templates(directory="templates")

CACHE = {}  # ключ = (coin_id, days), значение = (timestamp, filename)
CACHE_TTL = 300  # 5 минут

def generate_crypto_plot(coin_id: str, filename: str, days: int = 7):
    path = f"static/plots/{filename}"

    try:
        link = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {"vs_currency": "usd", "days": days, "interval": "daily"}
        response = requests.get(link, params=params)
        response.raise_for_status()

        data = response.json()
        if "prices" not in data:
            print(f"[{coin_id}] Ошибка: в ответе API нет ключа 'prices': {data}")
            return False

        prices = data["prices"]
        dates = [datetime.fromtimestamp(ts/1000) for ts, _ in prices]
        values = [price for _, price in prices]

        plt.figure(figsize=(8, 4))
        plt.style.use("dark_background")
        plt.plot(dates, values, linewidth=3, color="#007aff")
        plt.title(f"{coin_id.capitalize()} Price ({days} Days)")
        plt.xticks(rotation=45)
        plt.tight_layout()

        os.makedirs("static/plots", exist_ok=True)
        plt.savefig(path, transparent=True, bbox_inches="tight")
        plt.close()

        return True

    except requests.exceptions.RequestException as e:
        print(f"[{coin_id}] Ошибка запроса к API: {e}")
        return False
    except Exception as e:
        print(f"[{coin_id}] Другая ошибка при создании графика: {e}")
        return False

def get_cached_plot(coin_id: str, days: int):
    key = (coin_id, days)
    now = time.time()

    # Проверяем кэш
    if key in CACHE and now - CACHE[key][0] < CACHE_TTL:
        return CACHE[key][1]

    # Генерируем график
    filename = f"{coin_id}_{days}d.png"
    success = generate_crypto_plot(coin_id, filename, days)
    if success:
        CACHE[key] = (now, filename)
        return filename
    else:
        return None

# def generate_crypto_plot(coin_id: str, filename: str, days: int):
#     # 1. Парсинг данных
#     link = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
#     params = {"vs_currency": "usd", "days": days, "interval": "daily"}
#     path = f"static/plots/{filename}"

#     try:
#         response = requests.get(link, params=params)
#         data = response.json()
#         prices = data["prices"]
        
#         dates = []
#         values = []
#         for timestamp, price in prices:
#             # Превращаем таймстамп в объект даты
#             dates.append(datetime.fromtimestamp(timestamp / 1000))
#             values.append(price)

#         # 2. Построение графика (теперь dates и values точно видны!)
#         plt.figure(figsize=(8, 4))
#         # Стилизация под Apple Dark Style
#         plt.style.use('dark_background') 
#         plt.plot(dates, values, color='#007aff', linewidth=3) 
        
#         # Делаем фон прозрачным
#         plt.gcf().patch.set_alpha(0)
#         plt.gca().patch.set_alpha(0)
#         plt.tight_layout()
#         plt.savefig(path, transparent=True, bbox_inches='tight')

#         plt.title(f"{coin_id.capitalize()} Price ({days} Days)")
#         plt.xticks(rotation=45)
#         plt.tight_layout()

#         # Проверяем папку
#         os.makedirs("static/plots", exist_ok=True)
        
#         # 3. Сохранение
#         plt.savefig(path, transparent=True, bbox_inches="tight")
#         plt.close() # Важно для очистки памяти
#         return True
#     except Exception as e:
#         print(f"Ошибка при создании графика: {e}")
#         return False
    