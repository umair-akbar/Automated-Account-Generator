import ast
import random
import requests
import string
from captcha_solver import captcha_solver

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/58.0.3029.110 Safari/537.36'}
url = 'https://secure.runescape.com/m=account-creation/create_account?theme=oldschool'
payload = {}
counter = 0  # counter for our acc creating loop. probably a better way to do this
proxy_list = open("proxy_list.txt", "r")
number_of_accounts = 2  # Number of accounts that we want to create


def get_proxy() -> dict:
    """Returns our next proxy to use"""
    proxy = {"https": (next(proxy_list))}
    return proxy


def access_page(proxy):
    """Returns the status of the page"""
    response = requests.get(url, proxies=proxy, headers=headers)

    if response.ok:
        print("Loaded page successfully. Continuing.")
        return True
    else:
        print(f"Failed to load page. Status code: {response}")
        return False


def get_payload(captcha) -> dict:
    """Generates and fills out our payload"""
    # Generate random email and password for the account
    email = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(6)])
    password = email + str(random.randint(1, 1000))
    email = email + '@gmail.com'
    # Generate random birthday for the account
    day = str(random.randint(1, 25))
    month = str(random.randint(1, 12))
    year = str(random.randint(1980, 2006))  # Make sure to be at least 13 years old

    payload = {
        'theme': 'oldschool',
        'email1': email,
        'onlyOneEmail': '1',
        'password1': password,
        'onlyOnePassword': '1',
        'day': day,
        'month': month,
        'year': year,
        'create-submit': 'create',
        'g-recaptcha-response': captcha
    }
    return payload


def format_payload(payload) -> str:
    """Neatly formats our payload data"""
    formatted_payload = (f"\nemail:{payload['email1']}, password:{payload['password1']},"
                         f" Birthday:{payload['month']}/{payload['day']}/{payload['year']}")

    return formatted_payload


def save_account(formatted_payload):
    """Save the needed account information to created_accs.txt"""
    with open("created_accs.txt", "a+") as acc_list:
        acc_list.write(formatted_payload)


def create_account(payload):
    """Creates our account and returns the registration info"""
    proxy = get_proxy()
    requests.session()
    if access_page(proxy):
        submit = requests.post(url, proxies=proxy, data=payload)
        if submit.ok:
            save_account(format_payload(payload) + '' + str(proxy))  # TODO: Format proxy with acc details correctly
            print(f"Created account and saved to created_accs.txt with the following details:"
                  f" {format_payload(payload)}\n")
        else:
            print(f"Creation failed. Error code {submit.status_code}")


while counter < number_of_accounts:
    counter += 1
    create_account(get_payload(captcha_solver()))
