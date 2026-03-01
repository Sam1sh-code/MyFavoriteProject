
import requests
from datetime import datetime
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Папка для сохранения графиков
PLOTS_DIR = "static/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# Кэш для графиков
PLOT_CACHE = {}
CACHE_TTL = 300  # 5 минут

def fetch_coin_data(coin: str, days: int):
    """
    Получаем данные из CoinGecko для указанной монеты и периода.
    Возвращаем список словарей с 'date' и 'price'.
    """
    link = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}
    
    try:
        response = requests.get(link, params=params)
        if response.status_code == 429:
            raise Exception("Rate limit exceeded. Try again later.")
        response.raise_for_status()
        data = response.json()
        
        if "prices" not in data:
            raise Exception(f"No 'prices' in API response for {coin} ({days} days)")

        formatted = [
            {"date": datetime.fromtimestamp(p[0]/1000).strftime("%d %b"), "price": p[1]}
            for p in data["prices"]
        ]
        return formatted
    except Exception as e:
        print(f"[fetch_coin_data error] {e}")
        return []

def generate_crypto_plot(coin: str, days: int, filename: str):
    """
    Генерация PNG графика для монеты и сохранение в static/plots
    """
    key = (coin, days)
    
    # Используем кэш
    if key in PLOT_CACHE:
        return PLOT_CACHE[key]

    data = fetch_coin_data(coin, days)
    if not data:
        return None

    dates = [d["date"] for d in data]
    prices = [d["price"] for d in data]

    plt.figure(figsize=(8,4))
    plt.style.use('dark_background')
    plt.plot(dates, prices, color="#007aff", linewidth=2)
    plt.xticks(rotation=45)
    plt.title(f"{coin.capitalize()} Price ({days}D)")
    plt.tight_layout()

    path = os.path.join(PLOTS_DIR, filename)
    plt.savefig(path, transparent=True)
    plt.close()

    # Сохраняем в кэш
    PLOT_CACHE[key] = filename
    return filename

def get_cached_plot(coin: str, days: int):
    """
    Возвращаем имя файла графика из кэша или создаем заново
    """
    filename = f"{coin}_{days}D.png"
    full_path = os.path.join(PLOTS_DIR, filename)
    if not os.path.exists(full_path):
        generate_crypto_plot(coin, days, filename)
    return filename
