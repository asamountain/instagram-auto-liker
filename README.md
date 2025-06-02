# Instagram Auto Liker

A Python-based automation tool to like Instagram posts automatically, either from your home feed or by searching hashtags.  
**No access token required.**  
**Currently supports home feed and hashtag-based liking.**

## Features

- Works with Python 2.7
- Uses Selenium with ChromeDriver for browser automation
- Supports multiple Instagram accounts (credentials stored locally)
- Can like posts from home feed or by hashtag search
- Optionally follows users when liking by hashtag
- Designed for Windows 10, 64-bit, Chrome Browser (ver. 73.0.3683.103)

## Setup

1. Install pip if not already installed:
   ```bash
   python get-pip.py
   ```
2. Install required Python packages:
   ```bash
   pip install pyglet selenium tinydb
   ```
3. Ensure `chromedriver.exe` matches your Chrome version and is in the project directory.

## Usage

1. Run the script:
   ```bash
   python run.py
   ```
2. Follow the prompts to add/select an account and choose a mode:
   - `h`: Like posts from your home feed
   - `t`: Like posts by searching hashtags

## File/Folder Structure

- `run.py`: Main automation script (see in-code comments for details)
- `account.json`: Stores Instagram account credentials and settings
- `get-pip.py`: Script to install pip
- `chromedriver.exe`: ChromeDriver binary for Selenium
- `debug.log`: Error logs from browser automation
- `.gitignore`: Files/folders ignored by git

## Security Note

- Credentials are stored in plain text in `account.json`. Do not share this file.
- Use at your own risk. Automation may violate Instagram's terms of service.

---

## For Developers & Hiring Managers

- The code is modular, with clear separation between account management, browser automation, and user interaction.
- Each function in `run.py` is documented with comments explaining its purpose.
- The project demonstrates practical use of Selenium, and Python scripting for automation tasks.
