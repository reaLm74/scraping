'''Парсер Автоальфа асинхронный'''
import asyncio
import csv
import time

import aiohttp
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/118.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;"
              "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7"
}


async def get_page_data(session, name, page, writer):
    url_page = f"https://avtoalfa.com/proizvoditeli/{name}?stock=nch,msk&{page}"
    async with session.get(url=url_page, headers=headers) as response:
        response_page = await response.text()
        data = BeautifulSoup(response_page, 'html.parser')
        product = data.find_all(
            "article",
            class_='relative group product flex flex-col pt-5 md:pt-0 '
                   'bg-white shadow-md hover:shadow-xl '
                   'transition-shadow sm:rounded-lg'
        )
        for item in product:
            brand = item.find('span').text
            article = item.find(
                'div',
                class_='flex items-center w-full mt-2 md:mt-0 md:w-auto gap-4'
            ).text.strip()
            description = item.find(
                'a', class_='line-clamp-2 hover:opacity-70 transition-opacity'
            ).text
            try:
                url = f"https://avtoalfa.com{item.find('img')['src']}"
            except:
                url = 'Изображение отсутствует'
            write = brand, article, description, url
            writer.writerow(write)


async def get_info(session, name, retry=5):
    start = time.perf_counter()
    try:
        url_brand = f"https://avtoalfa.com/proizvoditeli/" \
                    f"{name['href']}?stock=nch,msk"
        response_brand = await session.get(url=url_brand, headers=headers)
    except:
        print(f'[INFO]')
        time.sleep(10)
        if retry:
            print(f'[INFO] retry={retry} => {name.text}')
            return get_info(session, name, retry=(retry - 1))
        else:
            return print(f'[INFO] retry={retry} не доступна')
    data = BeautifulSoup(await response_brand.text(), 'html.parser')
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
        tasks = []
        for page in range(1, pages + 1):
            task = asyncio.create_task(
                get_page_data(session, name['href'], page, writer))
            tasks.append(task)
        await asyncio.gather(*tasks)
    spend = time.perf_counter() - start
    print(
        f'[+] Загружен производитель: '
        f'"{name.text}". Затрачено: {spend:0.2f} сек.'
    )


async def get_id_manufacturers():
    async with aiohttp.ClientSession() as session:
        url = f'https://avtoalfa.com/proizvoditeli/'
        response = await session.get(url=url, headers=headers)
        data = BeautifulSoup(await response.text(), 'html.parser')
        all_data = data.find_all("div", class_="manufactors2__row-item")
        tasks = []
        start = 0
        for num in range(0, len(all_data), 18):
            for item in all_data[start:num]:
                task = asyncio.create_task(get_info(session, item.a))
                tasks.append(task)
            await asyncio.gather(*tasks)
            start = num


def main():
    start = time.perf_counter()
    asyncio.get_event_loop().run_until_complete(get_id_manufacturers())
    print(f'Общее время работы: {time.perf_counter() - start:0.2f}')


if __name__ == '__main__':
    main()
