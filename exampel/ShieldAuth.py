import os
import sys
import time
import json
import logging
import pyotp
import qrcode
import pyttsx3
import hashlib
import uuid
import getpass
import random
import string
import requests

# Setup logging
logging.basicConfig(
    filename='special_2fa_generator.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_machine_id():
    """
    Get a unique machine ID for device fingerprinting.
    """
    # Use uuid.getnode() to get MAC address as machine ID
    machine_id = uuid.getnode()
    machine_id_hash = hashlib.sha256(str(machine_id).encode()).hexdigest()
    logging.info(f"Machine ID hash: {machine_id_hash}")
    return machine_id_hash

def get_location():
    """
    Get user's current city and country using an IP geolocation API.
    """
    try:
        response = requests.get('https://ipinfo.io/json')
        if response.status_code == 200:
            data = response.json()
            city = data.get('city', 'Unknown')
            country = data.get('country', 'Unknown')
            logging.info(f"User location: {city}, {country}")
            return city, country
        else:
            logging.warning("Failed to get location info from API")
            return None, None
    except Exception as e:
        logging.error(f"Error getting location: {e}")
        return None, None

import hashlib

def generate_backup_code(length=8):
    """
    Generate a single emergency backup code.
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def save_backup_codes(codes_dict, filename='backup_codes.json'):
    """
    Save backup codes dictionary to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(codes_dict, f, indent=4)
    logging.info(f"Backup codes saved to {filename}")

def load_backup_codes(filename='backup_codes.json'):
    """
    Load backup codes dictionary from a JSON file.
    """
    if not os.path.exists(filename):
        return {}
    with open(filename, 'r') as f:
        data = json.load(f)
        return data

def get_backup_code_for_passphrase(passphrase, filename='backup_codes.json'):
    """
    Retrieve or generate a backup code for the given passphrase.
    Backup codes are stored as a dict with hashed passphrase keys.
    """
    codes_dict = load_backup_codes(filename)
    passphrase_hash = hashlib.sha256(passphrase.encode()).hexdigest()
    if passphrase_hash in codes_dict:
        return codes_dict[passphrase_hash]
    else:
        new_code = generate_backup_code()
        codes_dict[passphrase_hash] = new_code
        save_backup_codes(codes_dict, filename)
        logging.info(f"Generated new backup code for passphrase hash {passphrase_hash}")
        return new_code

def use_backup_code(code, filename='backup_codes.json'):
    """
    Mark a backup code as used by removing it from the dictionary.
    """
    codes_dict = load_backup_codes(filename)
    for key, value in list(codes_dict.items()):
        if value == code:
            del codes_dict[key]
            save_backup_codes(codes_dict, filename)
            logging.info(f"Backup code used: {code}")
            return True
    logging.warning(f"Attempted to use invalid or already used backup code: {code}")
    return False

def generate_qr_code(secret, filename='qrcode.png'):
    """
    Generate a QR code for the TOTP secret for easy Authenticator app setup.
    """
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name="user@example.com", issuer_name="Special2FA")
    img = qrcode.make(totp_uri)
    img.save(filename)
    logging.info(f"QR code generated and saved to {filename}")

def speak_otp(otp):
    """
    Speak the OTP aloud using pyttsx3.
    Suppress known ReferenceError from espeak driver callback.
    """
    try:
        engine = pyttsx3.init()
        # Spell out digits for clearer speech
        spelled_out = ' '.join(list(otp))
        engine.say(f"Your one time password is {spelled_out}")
        engine.runAndWait()
        logging.info("Spoken OTP aloud")
    except ReferenceError:
        # Suppress weakly-referenced object no longer exists error
        logging.warning("Suppressed ReferenceError in pyttsx3 espeak callback")

import argparse

import argparse

def main():
    parser = argparse.ArgumentParser(description="Special 2FA Generator")
    parser.add_argument('--speak', dest='speak', action='store_true',
                        help='Speak OTP aloud')
    parser.add_argument('--no-speak', dest='speak', action='store_false', default=True,
                        help='Disable speaking OTP aloud (default)')
    args = parser.parse_args()

    logging.info("Special 2FA Generator started")

    # Get machine ID and verify device fingerprint
    machine_id_hash = get_machine_id()

    # Get user location
    city, country = get_location()
    if city is None or country is None:
        city = "Unknown"
        country = "Unknown"
        print("Warning: Could not verify your location.")
        logging.warning("Location verification failed or unavailable.")

    # Display welcome banner and status BEFORE passphrase prompt
    logo = r"""
            ____  _     _      _     _         _         _   _     
           / ___|| |__ (_) ___| | __| |       / \  _   _| |_| |__  
           \___ \| '_ \| |/ _ \ |/ _` |_____ / _ \| | | | __| '_ \ 
            ___) | | | | |  __/ | (_| |_____/ ___ \ |_| | |_| | | |
           |____/|_| |_|_|\___|_|\__,_|    /_/   \_\__,_|\__|_| |_|
                                                                
|----------------------------------------------------------------------------|
| Created By: Sayantan Saha                                                  |
| Checkout my LinkedIn: https: https://www.linkedin.com/in/mastersayantan/   |
| Lookup at my GitHub Account : https://github.com/MasterSayantan            |
|----------------------------------------------------------------------------|
    """
    # Print logo in cyan color using ANSI escape codes
    print("\033[96m" + logo + "\033[0m")
    print("✔ Device Verified")
    print(f"✔ Location Verified ({city}, {country})")
    print()

    # Require user passphrase before showing OTP
    passphrase = getpass.getpass("Enter your passphrase: ")
    # For demo purposes, we just check if passphrase is non-empty
    if not passphrase:
        print("Passphrase is required. Exiting.")
        logging.warning("User did not enter passphrase. Exiting.")
        sys.exit(1)

    print("✔ Passphrase Accepted")
    print()

    # Generate TOTP secret bound to machine ID hash
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)

    # Generate QR code for Authenticator app setup
    generate_qr_code(secret)

    # Get or generate emergency backup code for this passphrase
    backup_code = get_backup_code_for_passphrase(passphrase)
    # Removed printing backup code here to avoid showing before welcome banner

    try:
        while True:
            otp = totp.now()
            print(f"🔐 Your OTP (valid for 30 seconds):  {otp}")
            if args.speak:
                print(f"📢 Speaking OTP aloud... \"{' '.join(list(otp))}\"")
                speak_otp(otp)
            print("\n(Next OTP refreshes automatically...)")
            print("-----------------------------------------")
            user_input = input("Need Help? Use your Emergency Backup Codes- ").strip().lower()
            if user_input == 'yes':
                print(f"\nYour Emergency Backup Codes- {backup_code}")
            # Wait for 30 seconds before refreshing OTP
            time.sleep(30)
            # Clear the console output for next display (works on Windows and Unix)
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
    except KeyboardInterrupt:
        print("\nExiting Special 2FA Generator.")
        logging.info("Special 2FA Generator finished by user interrupt.")


if __name__ == "__main__":
    main()
