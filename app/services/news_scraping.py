import requests
from datetime import datetime
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import fake_useragent
from bs4 import BeautifulSoup

def get_bbc_news():
    fuser = fake_useragent.UserAgent().random
    headers = {'user-agent': fuser}
    link = 'https://www.bbc.com/news'
    
    req = requests.get(link, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")

    news_list = []  # <--- Создаем пустой список для сбора данных

    section_title_node = soup.find('h2', {'data-testid': 'nevada-title'})

    if section_title_node:
        parent_section = section_title_node.find_parent('div', class_='sc-93f35dd3-2')
        grid = parent_section.find_next_sibling('div', {'data-testid': True})

        if grid:
            cards = grid.find_all('div', {'data-testid': 'dundee-card'})
            for card in cards:
                headline = card.find('h2', {'data-testid': 'card-headline'})
                link_tag = card.find('a', href=True)
                img_tag = card.find('img')

                if headline and link_tag:
                    # Вместо print, добавляем данные в список
                    news_list.append({
                        "title": headline.get_text(strip=True),
                        "url": f"https://www.bbc.com{link_tag['href']}",
                        "image": img_tag['src'] if img_tag else "https://via.placeholder.com/300"
                    })
    
    return news_list  # <--- ОБЯЗАТЕЛЬНО возвращаем результат!

# def get_bbc_news():
#     fuser = fake_useragent.UserAgent().random
#     headers = {'user-agent':fuser}

#     link = 'https://www.bbc.com/news'

#     req = requests.get(link, headers=headers)

#     soup = BeautifulSoup(req.text, "lxml")
#     # Сохраняем
#     with open("bbc_news.html", "w", encoding="utf-8") as file:
#         file.write(soup.prettify())

#     with open("bbc_news.html", "r", encoding="utf-8") as file:
#         src = file.read()

#     soup = BeautifulSoup(src, "lxml")

#     soup = BeautifulSoup(src, "lxml")

#     # 1. Ищем заголовок секции (напр. Iran war)
#     # Используем data-testid, это надежнее классов
#     section_title_node = soup.find('h2', {'data-testid': 'nevada-title'})

#     if section_title_node:
#         section_name = section_title_node.get_text(strip=True)
        

#         # 2. Переходим к родительскому контейнеру всей секции
#         # Мы поднимаемся вверх до общего блока, который содержит и заголовок, и новости
#         parent_section = section_title_node.find_parent('div', class_='sc-93f35dd3-2')
        
#         # 3. Теперь ищем блок с новостями, который идет СРАЗУ после заголовка
#         # В твоем коде это блок с data-testid="nevada-grid-5"
#         grid = parent_section.find_next_sibling('div', {'data-testid': True})

#         if grid:
#             # 4. Ищем все карточки новостей внутри этой сетки
#             cards = grid.find_all('div', {'data-testid': 'dundee-card'})

#             for card in cards:
#                 # Находим заголовок новости
#                 headline = card.find('h2', {'data-testid': 'card-headline'})
#                 # Находим ссылку (она выше по дереву внутри карточки)
#                 link_tag = card.find('a', href=True)

#                 if headline and link_tag:
#                     title = headline.get_text(strip=True)
#                     # BBC часто дает относительные ссылки (/news/...), добавляем домен
#                     full_url = f"https://www.bbc.com{link_tag['href']}"
                    
#                     print(f"Новость: {title}")
#                     print(f"Ссылка: {full_url}")
#                     print("-" * 20)
    
# Ищем все заголовки h2
# headlines = soup.find_all('h2', class_="sc-93f35dd3-4 cPmpei")

# for line in headlines:
#     print(line.get_text(strip=True))

# for i, headline in enumerate(headlines, 1):
    # text = headline.get_text(strip=True)
    # if text: # Проверяем, что заголовок не пустой
        # print(f"{i}. {text}")