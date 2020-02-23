# osrs_acc_creator
Account creator personal project for the game Old School Runescape

Uses POST requests to create Old School Runescape accounts with 2captcha integration to bypass Recaptcha as well as proxy support.

How to use:

Add your 2captcha API key to api_key in captcha_solver.py

add your list of proxies to proxy_list.txt in the format: socks5://USERNAME:PASSWORD@PROXYIP:PROXYPORT

change number_of_accounts in acc_creator.py to how many accounts you'd like to create

_____________________________________________________________________

HOW TO USE:

1. Open and edit settings.ini to fit your use case.

2. Run acc_creator.py

3. List of created accounts will save to created_accs.txt
