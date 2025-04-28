# Shield-Auth

Shield-Auth is a command-line tool that provides a secure two-factor authentication (2FA) solution with enhanced features such as device fingerprinting, location verification, emergency backup codes, and audible OTP announcements.

## Features

- **Device Fingerprinting:** Uses the machine's MAC address hashed to uniquely identify the device.
- **Location Verification:** Retrieves the user's current city and country using IP geolocation.
- **Passphrase Protection:** Requires a user passphrase before generating OTPs.
- **Time-based One-Time Password (TOTP):** Generates OTPs valid for 30 seconds compatible with standard authenticator apps.
- **QR Code Generation:** Creates a QR code for easy setup with authenticator apps.
- **Emergency Backup Codes:** Generates a unique emergency backup code per passphrase, stored securely and retrievable on demand.
- **Audible OTP:** Speaks the OTP aloud for accessibility.
- **Interactive CLI:** Prompts the user to display emergency backup codes only when needed.

![image](https://github.com/MasterSayantan/Shield-Auth/blob/main/test.png)  

## Installation

### Prerequisites

- Python 3.6 or higher
- `pip` package manager

### Required Python Packages

The following Python packages are required:

- pyotp
- qrcode
- pyttsx3
- requests

You can install them using the provided `requirements.txt` file.

### Installation Steps on Linux

1. Clone or download the repository to your local machine.

2. Open a terminal and navigate to the project directory.

3. (Optional) It is recommended to create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the required packages:

   ```bash
   git clone https://github.com/MasterSayantan/Shield-Auth.git
   cd Shield-Auth
   pip install -r requirements.txt
   ```

5. Run the Shield-Auth:

   ```bash
   python3 ShieldAuth.py --speak
   ```
   if you use linux system then- 
   ```bash
   python3 ShieldAuth.py --no-speak
   ```

## Usage

1. Run the program.

2. The CLI logo and device/location verification status will be displayed.

3. Enter your passphrase when prompted.

4. The program will generate and display a TOTP code every 30 seconds.

5. By default, speaking the OTP aloud is disabled on Linux systems to avoid known issues with the pyttsx3 espeak driver. You can enable or disable this feature using the following command line options:

   - `--speak` : Enable speaking OTP aloud (applicable for Windows and other systems).
   - `--no-speak` : Disable speaking OTP aloud (default on Linux systems).

6. When prompted, you can choose to view your emergency backup code by typing "yes".

7. To exit, press `Ctrl+C`.

## Notes

- Emergency backup codes are stored hashed by passphrase in `backup_codes.json`.
- The QR code for authenticator app setup is saved as `qrcode.png`.
- Logs are saved in `special_2fa_generator.log`.

## Author

Sayantan Saha  
- LinkedIn: https://www.linkedin.com/in/mastersayantan/  
- GitHub: https://github.com/MasterSayantan
