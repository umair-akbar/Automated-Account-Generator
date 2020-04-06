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


def use_tribot(charname, charpass):
    tribot_username = get_settings_variables()[9]
    tribot_password = get_settings_variables()[10]
    script_to_use = get_settings_variables()[11]
    script_args = get_settings_variables()[12]

    original_path = os.getcwd()
    client = find_tribot()
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
