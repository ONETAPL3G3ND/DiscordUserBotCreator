import g4f
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from g4f.client import Client
from hcaptcha_solver import hcaptcha_solver
import time


def register_discord_account(email, username, global_name, password, day, month, year, invites_link, proxy):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")  # Максимизировать окно браузера
        options.add_argument(f'--proxy-server={proxy}')
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        client = Client()

        driver.get("https://discord.com/register")
        time.sleep(4)  # Пауза для загрузки страницы

        # Заполнение полей регистрации
        email_field = driver.find_element(By.NAME, "email")
        email_field.send_keys(email)

        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys(username)

        agree_checkbox = driver.find_element(By.NAME, "global_name")
        agree_checkbox.send_keys(global_name)

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(password)

        day_set = driver.find_element(By.XPATH, "//*[@id=\"react-select-2-input\"]")
        day_set.send_keys(day)
        day_set.send_keys(Keys.ENTER)

        month_set = driver.find_element(By.XPATH, "//*[@id=\"react-select-3-input\"]")
        month_set.send_keys(month)
        month_set.send_keys(Keys.ENTER)

        year_set = driver.find_element(By.XPATH, "//*[@id=\"react-select-4-input\"]")
        year_set.send_keys(year)
        year_set.send_keys(Keys.ENTER)

        agree_checkbox = driver.find_element(By.XPATH,
                                             "//*[@id=\"app-mount\"]/div[2]/div[1]/div[1]/div/div/div/form/div[2]/div/div[7]/label/input")
        agree_checkbox.click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))).click()

        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//iframe[contains(@src,'hcaptcha') and contains(@src,'checkbox')]"))).click()

        driver.switch_to.default_content()
        wait.until(EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH, "//iframe[contains(@src,'hcaptcha') and contains(@src,'challenge')]")))

        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@id, 'menu-info')]"))).click()

        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@id, 'text_challenge')]"))).click()

        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'button-submit button')]")))
        button_text = submit_button.find_element(By.XPATH, "./*").text

        while True:
            try:
                text_div = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@id, 'prompt-text')]")))
                text = text_div.find_element(By.XPATH, "./*").text

                print(text)
                response = client.chat.completions.create(
                    model=g4f.models.gpt_4_turbo,
                    messages=[{"role": "user", "content": f"ОТВЕТЬ ТОЛЬКО \"да\" или \"нет\": {text}"}]
                )

                answer = str(response.choices[0].message.content.lower().replace(".", "").replace("\n", ""))
                print(answer)
                input_text = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'input-field')]")))
                input_text.click()
                input_text.send_keys(answer)
                time.sleep(10)
                submit_button.click()
            except:
                break
        for invite_link in invites_link:
            driver.get(invite_link)
            time.sleep(3)
            driver.find_element(By.XPATH, "//*[@id=\"app-mount\"]/div[2]/div[1]/div[1]/div/div/div/section/div[2]/button")
            time.sleep(4)
        return True
        driver.quit()
    except Exception as e:
        print(e)
        return False


