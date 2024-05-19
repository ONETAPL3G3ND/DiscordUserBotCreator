import requests

class Grabber:

    def GetDiscordToken(self, username, password):
        url = "https://discord.com/api/v9/auth/login"

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        }

        payload = {
            "login": username,
            "password": password,
            "undelete": False,
            "captcha_key": None,
            "login_source": None,
            "gift_code_sku_id": None
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            token = response.json().get("token")
            if token:
                with open("tokens.txt", "a") as f:
                    f.write(token + "\n")
            else:
                print("Токен не найден в ответе.")
        else:
            print("Не удалось войти в аккаунт. Код ответа:", response.status_code)


