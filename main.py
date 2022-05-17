import os

import requests
from fake_useragent import UserAgent
from pyfiglet import Figlet


UA = UserAgent(verify_ssl=True)
URL = "https://public-sonjj.p.rapidapi.com/email-checker"

headers = {
    'X-RapidAPI-Host': 'public-sonjj.p.rapidapi.com',
    'X-RapidAPI-Key': 'f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081',
    'Accept': '*/*',
    'User-Agent': f'{UA.random}'
}

dir_path = os.path.join(os.getcwd(), 'processed_emails')

if not os.path.exists(dir_path):
    os.mkdir(dir_path)

title = Figlet(font='chunky')
print(title.renderText('e-Mail  checker'))

file_input = str(input('Enter file name: '))


def proxy_mover(number: int) -> dict:
    """
    Function moves on proxy an return it
    :param number: number of proxy
    :return: dict with proxy
    """
    with open('proxy.txt', 'r') as proxy:
        proxy_list = [x.replace('\n', '') for x in proxy]
        if number <= len(proxy_list):
            proxies = {
                'https': f'http://{proxy_list[number]}'
            }
            return proxies

        else:
            proxies = {
                'https': f'http://{proxy_list[number]}'
            }
            return proxies


def main() -> None:
    """
    Checker email, with use api 'ychecker.com'
    :return: None
    """
    with open(f'{file_input}', 'r') as doc:
        total = 0
        count = 0
        number = 0
        for check_line in doc:
            poor_email = check_line.split(';')[0]

            if count == 100:
                with open('used_proxy.txt', 'a') as used:
                    used.write(f'\n{proxy.values()}')

                count = 0
                number += 1
            else:
                count += 1

            proxy = proxy_mover(number=number)

            r = requests.get(f'https://ychecker.com/app/key?email={poor_email}', proxies=proxy)
            poor_key = r.text.split(',')[-1].split(':')[-1].replace('"}', '').replace('"', '')

            querystring = {
                'email': f'{poor_email}',
                'key': f'{poor_key}'
            }

            response = requests.request("GET", URL, headers=headers, params=querystring)

            try:
                poor_state = response.text.split(',')[3].split(':')[-1].replace('"', '')
                if poor_state == 'VerifyPhone':
                    with open(os.path.join(dir_path, 'verify_phone.txt'), 'a') as file:
                        file.write(f'{check_line}\n')
                elif poor_state == 'NotExist':
                    with open(os.path.join(dir_path, 'not_exist.txt'), 'a') as file:
                        file.write(f'{check_line}\n')
                elif poor_state == 'Disable':
                    with open(os.path.join(dir_path, 'disable.txt'), 'a') as file:
                        file.write(f'{check_line}\n')
                elif poor_state == 'Disable|NotExist':
                    with open(os.path.join(dir_path, 'disable_or_not_exist.txt'), 'a') as file:
                        file.write(f'{check_line}\n')
                elif poor_state == 'Ok':
                    with open(os.path.join(dir_path, 'ok.txt'), 'a') as file:
                        file.write(f'{check_line}\n')

                with open(os.path.join(dir_path, 'log.txt'), 'a') as log:
                    log.write(f'{response.text}\n')
            except IndexError:
                print('Too many requests for this ip')
                with open(os.path.join(dir_path, 'log.txt'), 'a') as log:
                    log.write(f'{response.text}\n')

            print(f'\nNumber of proxy: {number}\t\t Proxy: {proxy}\t\t Processed emails: {count}')
            print(response.text)
            total += 1
        print('Checking emails is completed!')


if __name__ == '__main__':
    main()
