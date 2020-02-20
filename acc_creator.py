import random
import requests
import string
import sys
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/58.0.3029.110 Safari/537.36'}
url = 'https://secure.runescape.com/m=account-creation/create_account?theme=oldschool'
payload = {}
counter = 0  # counter for our acc creating loop. probably a better way to do this
number_of_accounts = 2  # Number of accounts that we want to create


def captcha_solver():
    """Handles and returns recaptcha answer"""
    api_key = '28603055fdf022735d1d83c9c0a1bbf1'  # 2captcha api key
    site_key = '6Lcsv3oUAAAAAGFhlKrkRb029OHio098bbeyi_Hv'  # osrs site key
    site_url = 'https://secure.runescape.com/m=account-creation/create_account?theme=oldschool'  # rs sign up page

    s = requests.Session()

    # here we post site key to 2captcha to get captcha ID (and we parse it here too)
    captcha_id = s.post(f"http://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={site_key}"
                        f"&pageurl={site_url}").text.split('|')[1]

    # then we parse gresponse from 2captcha response
    recaptcha_answer = s.get(
        f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}").text
    print("Solving captcha...")
    while 'CAPCHA_NOT_READY' in recaptcha_answer:
        sleep(5)
        recaptcha_answer = s.get(
            f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}").text
    recaptcha_answer = recaptcha_answer.split('|')[1]

    return recaptcha_answer


def access_page():
    """Returns the status of the page"""
    global response
    response = requests.get(url, headers=headers)

    if response.ok:
        print("Loaded page successfully. Continuing.")
        return True
    else:
        print(f"Failed to load page. Status code: {response}")
        return False


def get_payload(captcha):
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

def format_payload(payload):
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
    requests.session()
    if access_page() == True:
        submit = requests.post(url, data=payload)
        if submit.ok:
            save_account(format_payload(payload))
            print(f"Created account and saved to created_accs.txt with the following details:"
                  f" {format_payload(payload)}\n")
        else:
            print(f"Creation failed. Error code {submit.status_code}")


while counter < number_of_accounts:
    counter += 1
    create_account(get_payload(captcha_solver()))
