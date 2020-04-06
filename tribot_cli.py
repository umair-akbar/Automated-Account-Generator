# Tribot CLI:
# https://help.tribot.org/support/solutions/articles/36000043771-how-to-use-cli-arguments-to-launch-tribot

import glob, os, subprocess
import getpass
import sys
try:
	from my_utilities import get_settings_variables
except ImportError:
	sys.exit("Couldn't import my_utilities.py. "
			 "Make sure it's in the same directory.")

def find_tribot():
    """
    Finds the user's tribot.jar for CLI use
    This currently only supports the default Windows path.
    TODO: Add support for mac and linux paths
    """
    user = getpass.getuser()
    path = (f"C:\\Users\\{user}\\AppData\\Roaming\\.tribot\\dependancies")

    print("")
    print ("Changing to our Tribot directory")
    os.chdir(path)
    print (os.getcwd())

    client = str(glob.glob('tribot*'))
    client = client[2:-2]
    print(f"Our Tribot client is called: {client}")

    return client

def get_index(input_string, sub_string, ordinal):
    current = -1
    for i in range(ordinal):
        current = input_string.index(sub_string, current + 1)
    return current

def format_current_proxy(proxy):
    """Formats and returns our current proxy for CLI use"""
    proxy = str(proxy)

    # Formatting shenanigans to get the strings we need for CLI usage
    proxy_username = proxy[get_index(proxy, '/', 2)+1:get_index(proxy, ':', 3)]
    proxy_password = proxy[get_index(proxy, ':', 3)+1:get_index(proxy, '@', 1)]
    proxy_ip = proxy[get_index(proxy, '@', 1)+1:get_index(proxy, ':', 4)]
    proxy_port = proxy[get_index(proxy, ':', 4)+1:get_index(proxy, "'", 4)]

    return proxy_username, proxy_password, proxy_ip, proxy_port

def use_tribot(charname, charpass, proxy=None):
    # Storing all of our settings while we're in the correct directory
    use_proxies = get_settings_variables()[0]
    tribot_username = get_settings_variables()[9]
    tribot_password = get_settings_variables()[10]
    script_to_use = get_settings_variables()[11]
    script_args = get_settings_variables()[12]

    if use_proxies:
        proxy_username = format_current_proxy(proxy)[0]
        proxy_password = format_current_proxy(proxy)[1]
        proxy_host = format_current_proxy(proxy)[2]
        proxy_port = format_current_proxy(proxy)[3]

    original_path = os.getcwd()
    client = find_tribot()

    # Create our CLI command according to if we're using proxies or not
    if use_proxies:
        cli_cmd = (f'java -jar {client} '
                f'--username "{tribot_username}" --password "{tribot_password}" '
                f'--charusername "{charname}" --charpassword "{charpass}" '
                f'--script "{script_to_use}" --charworld "433" '
                f'--proxyhost "{proxy_host}" '
                f'--proxyport "{proxy_port}" '
                f'--proxyusername "{proxy_username}" '
                f'--proxypassword "{proxy_password}" ')
    else:
        cli_cmd = (f'java -jar {client} '
            f'--username "{tribot_username}" --password "{tribot_password}" '
            f'--charusername "{charname}" --charpassword "{charpass}" '
            f'--script "{script_to_use}" --charworld "433"')

    print("")
    print("\nLoading tribot with the following settings...")
    print(cli_cmd)

    # Run the Tribot CLI in a separate, hidden shell to decrease clutter
    CREATE_NO_WINDOW = 0x08000000
    subprocess.Popen(f"start /B start cmd.exe @cmd /k {cli_cmd}", shell=True, 
                    creationflags=CREATE_NO_WINDOW)
    
    # Changing back to the account creator directory
    # So we can see the settings.ini file for the next account.
    print (f"Changing our directory back to {original_path}")
    os.chdir(original_path)
