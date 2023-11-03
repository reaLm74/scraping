'''Парсер Автоальфа синхронный'''
import csv
import time

import requests
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}


def get_info(name):
    url_brand = f"https://avtoalfa.com/proizvoditeli/{name}"
    response_brand = requests.get(url_brand, headers=headers)
    data = BeautifulSoup(response_brand.text, 'html.parser')
    try:
        pages = int(data.find('a', {'title': 'Последняя'}).text)
    except:
        try:
            pages = int(data.find(
                'div', class_='flex flex-nowrap gap-[8px] text-grey'
            ).find_all('a')[-1].text)
        except:
            pages = 1
    with open('products.csv', 'a', encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        for page in range(1, pages + 1):
            try:
                url_page = f"https://avtoalfa.com/proizvoditeli/" \
                           f"{name}?page={page}"
                response_page = requests.get(url_page, headers=headers)
            except:
                continue
            data = BeautifulSoup(response_page.text, 'html.parser')
            product = data.find_all(
                "article",
                class_='relative group product flex flex-col '
                       'pt-5 md:pt-0 bg-white shadow-md hover:shadow-xl '
                       'transition-shadow sm:rounded-lg')
            for item in product:
                brand = item.find('span').text
                article = item.find(
                    'div',
                    class_='flex items-center w-full '
                           'mt-2 md:mt-0 md:w-auto gap-4'
                ).text.strip()
                description = item.find(
                    'a',
                    class_='line-clamp-2 hover:opacity-70 transition-opacity'
                ).text
                try:
                    url = f"https://avtoalfa.com{item.find('img')['src']}"
                except:
                    url = 'Изображение отсутствует'
                write = brand, article, description, url
                writer.writerow(write)


def get_id_manufacturers(response):
    data = BeautifulSoup(response.text, 'html.parser')
    all_data = data.find_all("div", class_="manufactors2__row-item")
    for item in all_data:
        start = time.perf_counter()
        get_info(item.a['href'])
        spend = time.perf_counter() - start
        print(
            f'[+] Загружен производитель: '
            f'"{item.a.text}". Затрачено: {spend:0.2f} сек.'
        )


def request_url():
    url = f'https://avtoalfa.com/proizvoditeli/'
    return requests.get(url, headers=headers)


def main():
    start = time.perf_counter()
    request = request_url()
    if request.status_code == 200:
        get_id_manufacturers(request)
    print(f'Общее время работы: {time.perf_counter() - start:0.2f}')


if __name__ == '__main__':
    main()
