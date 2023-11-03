from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup


def get_life_score():
    try:
        driver = webdriver.Chrome()
        driver.get('https://www.flashscorekz.com/football/')
        life = driver.find_elements(By.CLASS_NAME, 'filters__text')
        time.sleep(2)
        life[1].click()
        time.sleep(1)
        driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        time.sleep(3)
        test_1 = driver.find_elements(By.CLASS_NAME, 'event__expander--close')
        time.sleep(3)
        for e in test_1:
            e.click()
            # time.sleep(1)
        with open('flashscore_selenium.html', 'w', encoding="utf-8") as file:
            file.write(driver.page_source)
        print("Запись прошла")
    finally:
        driver.quit()

    with open('flashscore_selenium.html', encoding="utf-8") as file:
        src = file.read()
        data = BeautifulSoup(src, 'html.parser')
        team_1 = data.find_all('div', class_='event__participant--home')
        team_2 = data.find_all('div', class_='event__participant--away')
        score_team_1 = data.find_all('div', class_='event__score--home')
        score_team_2 = data.find_all('div', class_='event__score--away')
        for mach in range(len(team_1)):
            print(
                f'Матч между командами: '
                f'{team_1[mach].text.replace("ГОЛ", "").strip()} '
                f'- {team_2[mach].text.replace("ГОЛ", "").strip()}'
            )
            print(
                f'Счет: {score_team_1[mach].text.strip()} '
                f'- {score_team_2[mach].text.strip()}'
            )
            print('--------------------------------------------------')
            print()


def main():
    start = time.perf_counter()
    get_life_score()
    print(f'Общее время работы: {time.perf_counter() - start:0.2f}')


if __name__ == '__main__':
    main()
