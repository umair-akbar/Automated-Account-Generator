from configparser import ConfigParser
import sys


def get_settings_variables():
    """Reads settings from settings.ini and returns them"""
    config = ConfigParser()
    try:
        config.read('settings.ini')
    except FileNotFoundError:
        sys.exit("settings.ini file not found. "
                 "Make sure it's in the same directory.")
    else:
    	# Return our [USER_SETTINGS]
        use_proxies = config['USER_SETTINGS'].getboolean('use_proxies')
        captcha_api_key = config['USER_SETTINGS'].get('2captcha_api_key')
        num_of_accs = config['USER_SETTINGS'].getint('num_of_accs')
        username_prefix = config['USER_SETTINGS'].get('username_prefix')
        password = config['USER_SETTINGS'].get('password')
        acc_details_format = config['USER_SETTINGS'].getboolean('acc_details_format')


         # Return our [SITE_SETTINGS]
        site_key = config['SITE_SETTINGS'].get('site_key')
        site_url = config['SITE_SETTINGS'].get('site_url')

        return (use_proxies, captcha_api_key, num_of_accs, site_key, site_url, 
                username_prefix, password, acc_details_format)