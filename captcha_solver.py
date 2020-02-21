import requests
from time import sleep


def captcha_solver():
    """Handles and returns recaptcha answer"""
    api_key = ''  # 2captcha api key
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
