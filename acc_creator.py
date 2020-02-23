import ast
import random
import requests
import string
from time import sleep
from my_utilities import get_settings_variables



headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/58.0.3029.110 Safari/537.36'}
url = 'https://secure.runescape.com/m=account-creation/create_account?theme=oldschool'
# payload = {}
counter = 0  # counter for our acc creating loop. probably a better way to do this
proxy_list = open("proxy_list.txt", "r")

# Settings pulled from get_settings_variables -> settings.ini file
NUM_OF_ACCS = get_settings_variables()[2]  # Number of accounts that we want to create
USE_PROXIES = get_settings_variables()[0]  # 1 for True or 0 for False from settings.ini


def get_proxy() -> dict:
    """Returns our next proxy to use from the proxy_list.txt file"""
    proxy = {"https": (next(proxy_list))}
    return proxy


def access_page(proxy):
    """Returns True if we were able to access the page or False if we got a request error"""
    response = requests.get(url, proxies=proxy, headers=headers)

    if response.ok:
        print(f"We'll make: {NUM_OF_ACCS} accounts.")
        print(f"Will we use proxies?: {USE_PROXIES}")
        print("Loaded page successfully. Continuing.")
        return True
    else:
        print(f"Failed to load page. Status code: {response}")
        return False


def captcha_solver():
    """Handles and returns recaptcha answer for osrs account creation page"""
    API_KEY = get_settings_variables()[1]  # 2captcha api key read from settings.ini
    SITE_KEY = '6Lcsv3oUAAAAAGFhlKrkRb029OHio098bbeyi_Hv'  # osrs site key
    SITE_URL = 'https://secure.runescape.com/m=account-creation/create_account?theme=oldschool'  # rs sign up page

    s = requests.Session()

    # here we post site key to 2captcha to get captcha ID (and we parse it here too)
    captcha_id = s.post(f"http://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={SITE_KEY}"
                        f"&pageurl={SITE_URL}").text.split('|')[1]

    # then we parse gresponse from 2captcha response
    recaptcha_answer = s.get(
        f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}").text
    print("Solving captcha...")
    while 'CAPCHA_NOT_READY' in recaptcha_answer:
        sleep(20)
        recaptcha_answer = s.get(
            f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}").text
    recaptcha_answer = recaptcha_answer.split('|')[1]

    return recaptcha_answer


def get_payload(captcha) -> dict:
    """Generates and fills out our payload.
       Returns payload as dict"""
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
    """Neatly formats our payload data and returns it"""
    formatted_payload = (f"\nemail:{payload['email1']}, password:{payload['password1']},"
                         f" Birthday:{payload['month']}/{payload['day']}/{payload['year']}")

    return formatted_payload


def check_account(submit):
    """Checks to make sure the account was successfully created"""
    submit_page = submit.text
    success = '<p>You can now begin your adventure with your new account.</p>'
    if submit_page.find(success):
        return True
    else:
        print (submit.text)
        return False


def save_account(formatted_payload):
    """Save the needed account information to created_accs.txt"""
    with open("created_accs.txt", "a+") as acc_list:
        acc_list.write(formatted_payload)


def create_account():
    """Creates our account and returns the registration info"""
    proxy = get_proxy()
    requests.session()
    if access_page(proxy):
        payload = get_payload(captcha_solver())
        submit = requests.post(url, proxies=proxy, data=payload)
        if submit.ok:
            if check_account(submit):
                save_account(format_payload(payload) + '' + str(proxy))  # TODO: Format proxy with acc details correctly
                print(f"Created account and saved to created_accs.txt with the following details:"
                      f" {format_payload(payload)}\n")
            else:
                print("We submitted our account creation but didn't get to the creation successful page.")
        else:
            print(f"Creation failed. Error code {submit.status_code}")


while counter < NUM_OF_ACCS:
    counter += 1
    create_account()
    