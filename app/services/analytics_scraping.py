import matplotlib
matplotlib.use('Agg') # Фикс: запрещаем Matplotlib пытаться открыть окно на сервере
import matplotlib.pyplot as plt
import requests
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

templates = Jinja2Templates(directory="templates")

def generate_crypto_plot(coin_id: str, filename: str):
    # 1. Парсинг данных
    link = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": 7, "interval": "daily"}
    
    try:
        response = requests.get(link, params=params)
        data = response.json()
        prices = data["prices"]
        
        dates = []
        values = []
        for timestamp, price in prices:
            # Превращаем таймстамп в объект даты
            dates.append(datetime.fromtimestamp(timestamp / 1000))
            values.append(price)

        # 2. Построение графика (теперь dates и values точно видны!)
        plt.figure(figsize=(8, 4))
        # Стилизация под Apple Dark Style
        plt.style.use('dark_background') 
        plt.plot(dates, values, color='#007aff', linewidth=3) 
        
        # Делаем фон прозрачным
        plt.gcf().patch.set_alpha(0)
        plt.gca().patch.set_alpha(0)
        plt.tight_layout()
        plt.savefig(path, transparent=True, bbox_inches='tight')

        plt.title(f"{coin_id.capitalize()} Price (7 Days)", color='white', pad=20)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Проверяем папку
        os.makedirs("static/plots", exist_ok=True)
        
        # 3. Сохранение
        path = f"static/plots/{filename}"
        plt.savefig(path, transparent=True)
        plt.close() # Важно для очистки памяти
        return True
    except Exception as e:
        print(f"Ошибка при создании графика: {e}")
        return False
    