import time
import re
import requests
from bs4 import BeautifulSoup

headers = {
    'authority': 'local-ruua.flashscore.ninja',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://www.flashscorekz.com',
    'referer': 'https://www.flashscorekz.com/',
    'sec-ch-ua': '"Chromium";v="118", '
                 '"Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/118.0.0.0 Safari/537.36',
    'x-fsign': 'SW9D1eZo',
    'x-geoip': '1',
}


def get_details_match(id_match):
    url = f'https://www.flashscorekz.com/match' \
          f'/{id_match}/#/match-summary/match-summary'
    response = requests.get(url, headers=headers)
    data = BeautifulSoup(response.text, 'html.parser')
    print('Детальная информация:')
    print(data.find('meta', {'name': 'og:description'})['content'])
    print(data.find('meta', {'name': 'og:title'})['content'])


    f = requests.get(
        f'https://local-ruua.flashscore.ninja/46/x/feed/df_sui_1_{id_match}',
        headers=headers
    ).text
    ind_first_command = f.rfind('INX÷')
    ind_second_command = f.rfind('IOX÷')
    if f.rfind('INX÷') != (-1):
        print(
            f'Счет: {f[ind_first_command + 4:ind_first_command + 5]} '
            f'- {f[ind_second_command + 4:ind_second_command + 5]}')
    else:
        print('Счет: 0 - 0')

    print('---------------------------------------------------------------')
    print()


def get_attr_match(mach):
    # Индекс страницы
    ind = mach.find('¬')
    # Достаем название команд
    temp = (re.sub(r'[^а-яА-Я]+', ' ', mach)).split()
    temp = " ".join(sorted(set(temp), key=temp.index))
    temp = re.sub(r'[А-Я]+?(?=$|[\s.,?!]+)', '', temp)
    words = temp.split('  ')
    print(f'id матча: {mach[:ind]}, Команды: {words[0]} - {words[1]}')
    print()
    get_details_match(mach[:ind])


def get_life_match(response):
    data = str(BeautifulSoup(response.text, 'html.parser'))
    temp = data.split('¬~AA÷')
    for mach in temp:
        try:
            mach.index('¬RW÷0¬AI÷y¬AX÷1¬AO÷')
            get_attr_match(mach)
        except:
            try:
                mach.index('¬RW÷0¬AI÷y¬AX÷0¬AO')
                get_attr_match(mach)
            except:
                continue


def request_url():
    url = 'https://local-ruua.flashscore.ninja/46/x/feed/f_1_0_5_ru-kz_1'
    return requests.get(url, headers=headers)


def main():
    start = time.perf_counter()
    response = request_url()
    if response.status_code == 200:
        get_life_match(response)
    print(f'Общее время работы: {time.perf_counter() - start:0.2f}')


if __name__ == '__main__':
    main()
