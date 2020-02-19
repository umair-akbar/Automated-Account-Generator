import sys
import requests
from time import sleep

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko)'
                 ' Chrome/58.0.3029.110 Safari/537.36'}
url = 'https://secure.runescape.com/m=account-creation/create_account?theme=oldschool'
payload = {}

def captcha_solver():
    """Handles and returns recaptcha answer"""
    api_key = '' #2captcha api key
    site_key = '6Lcsv3oUAAAAAGFhlKrkRb029OHio098bbeyi_Hv' #osrs site key
    site_url = 'https://secure.runescape.com/m=account-creation/create_account?theme=oldschool' #rs sign up page

    s = requests.Session()

    # here we post site key to 2captcha to get captcha ID (and we parse it here too)
    captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(
        api_key, site_key, site_url)).text.split('|')[1]

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
        print ("Loaded page successfully. Continuing.")
        return True
    else:
        print (f"Failed to load page. Status code: {response}")
        return False

def get_payload(captcha):
    """fills out our payload"""
    payload = {
        'theme': 'oldschool',
        'email1': 'test995@google.com',
        'onlyOneEmail': '1',
        'password1': 'gavin1996',
        'onlyOnePassword': '1',
        'day': '15',
        'month': '06',
        'year': '1992',
        'create-submit': 'create',
        'g-recaptcha-response': captcha
    }
    return payload

def create_account(payload):
    """Creates our account and returns the registration info"""
    requests.session()
    if access_page() == True:
        submit = requests.post(url, data=payload)
        if submit.ok:
            print (f"Created account with the following details: \n {payload}")
        else:
            print (f"Creation failed. Error code {submit.status_code}")


create_account(get_payload(captcha_solver()))
