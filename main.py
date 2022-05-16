import requests
import os

# Creating directory
dir_path = os.path.join(os.getcwd(), 'processed_emails')

if not os.path.exists(dir_path):
    os.mkdir(dir_path)

url = "https://public-sonjj.p.rapidapi.com/email-checker"

file_input = str(input('Enter file name: '))


def main() -> None:
    """
    Checker email, with use api 'ychecker.com'
    :return: None
    """
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
        print('Checking emails is completed!')


if __name__ == '__main__':
    main()
