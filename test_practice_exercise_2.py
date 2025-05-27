from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_create_and_delete_card():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = r"C:\Users\T-X\Downloads\chrome-win64\chrome-win64\chrome.exe"  # твой Chrome 94
    chrome_options.add_argument('--window-size=1080,720')

    service = Service(executable_path=r"C:\Users\T-X\Downloads\chrome-win64\chromedriver-win64\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://qa-mesto.praktikum-services.ru")

        # Вход в профиль
        driver.find_element(By.ID, "email").send_keys("ura@ya.ru")
        driver.find_element(By.ID, "password").send_keys("12345678")
        driver.find_element(By.XPATH, "//button[text()='Войти']").click()

        # Ожидание для загрузки страницы профиля
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "profile__description")))

        # Клик на аватар по Class
        titles = driver.find_elements(By.CLASS_NAME, "card__title")
        title_before = titles[0].text

        # Создание новой карточки
        driver.find_element(By.CLASS_NAME, "profile__add-button").click()
        new_title = "Москва 12:25:36-27.05.2025"
        driver.find_element(By.CSS_SELECTOR, ".popup__input.popup__input_type_card-name").send_keys(new_title)
        driver.find_element(By.CSS_SELECTOR, ".popup__input.popup__input_type_url").send_keys('https://code.s3.yandex.net/qa-automation-engineer/python/files/photoSelenium.jpeg')
        driver.find_element(By.XPATH, "//form[@name='new-card']//button[text()='Сохранить']").click()

        # Ожидание появления новой карточки
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[contains(@class, 'card__delete-button') and not(contains(@class, 'card__delete-button_hidden'))]")
            )
        )

        # Проверяем что отображается верный тайтл на карточке
        titles = driver.find_elements(By.CLASS_NAME, "card__title")
        assert titles[-1].text == new_title

        # Ищем карточки и запоминаем количество
        cards = driver.find_elements(By.CLASS_NAME, "card")
        count_before = len(cards)

        # Удаляем созданную карточку
        delete_seach_button = driver.find_elements(By.CLASS_NAME, "card__delete-button")
        delete_seach_button[0].click()

        WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "card__title"), title_before
            )
        )

        # Проверяем уменьшение карточек
        WebDriverWait(driver, 30).until(
            lambda d: len(d.find_elements(By.CLASS_NAME, "card")) == count_before - 1
        )
        cards_after = driver.find_elements(By.CLASS_NAME, "card")

    finally:
        driver.quit()
