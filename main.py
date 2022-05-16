import requests
import os

# Creating directory
dir_path = f'{os.getcwd()}/processed_emails'

if not os.path.exists(dir_path):
    os.mkdir(dir_path)

url = "https://public-sonjj.p.rapidapi.com/email-checker"

file_input = str(input('Enter file name: '))

with open(f'{file_input}', 'r') as doc:
    for check_line in doc:
        poor_email = check_line.split(';')[0]

        r = requests.get(f'https://ychecker.com/app/key?email={poor_email}')
        poor_key = r.text.split(',')[-1].split(':')[-1].replace('"}', '').replace('"', '')

        querystring = {
            'email': f'{poor_email}',
            'key': f'{poor_key}'
        }

        headers = {
            "X-RapidAPI-Host": "public-sonjj.p.rapidapi.com",
            "X-RapidAPI-Key": "f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(f'{response.text}')
