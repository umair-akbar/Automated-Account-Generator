from configparser import ConfigParser


def get_settings_variables():
    """Reads settings from settings.ini and returns them"""
    config = ConfigParser()
    config.read('settings.ini')

    use_proxies = config['SETTINGS'].getboolean('use_proxies')
    captcha_api_key = config['SETTINGS'].get('2captcha_api_key')
    num_of_accs = config['SETTINGS'].getint('num_of_accs')

    return use_proxies, captcha_api_key, num_of_accs
