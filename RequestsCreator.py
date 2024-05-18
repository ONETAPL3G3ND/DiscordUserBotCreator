import requests
from veilcord import Solver

def create_discord_account(email, username, password, date_of_birth):
    url = "https://discord.com/api/v9/auth/register"
    session = requests.session()

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    cookies = {
        'locale': 'en-US'
    }

    payload = {
        "email": email,
        "username": username,
        "password": password,
        "date_of_birth": date_of_birth,
        "gift_code_sku_id": None,
        "invite": None,
        "consent": True,
        "captcha_key": None
    }

    response = session.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Аккаунт успешно создан.")
    else:
        print(f"Ошибка при создании аккаунта: {response.status_code}")
        print(response.json())
        captchaService = "CAPSOLVER"
        key = 'CAI-B84C18E3DC8EA33F8E46E171B9E8C152'
        capKey = Solver(session=session, cap_key=captchaService, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36").solve_captcha()
        print(capKey)


