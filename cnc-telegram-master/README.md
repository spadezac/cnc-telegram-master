# Command and Control Telegram Bot

*Disclaimer: This tool is for educational purposes only. Deploying it on any system without explicit, written authorization from the owner is illegal and unethical.*

A Python 3 demonstration of a Command and Control (C&C) bot that uses the Telegram API for secure, remote administration.

## Features
-   **Secure Access**: Bot usage is restricted to a pre-defined list of authorized Telegram user IDs.
-   **File System Operations**: List directory contents (`ls`), write to files (`write`), and download files (`download`).
-   **System Monitoring**: View active users (`users`) and running processes (`processes`).
-   **Remote Execution**: Execute arbitrary shell commands (`exec`) on the host machine.

## Setup Instructions
1.  **Get Telegram Credentials**:
    * Talk to `@BotFather` on Telegram to create a new bot and get your **API Token**.
    * Talk to `@userinfobot` on Telegram to get your numeric **User ID**.

2.  **Configure Authorization**:
    * Open the `authorization.py` file.
    * Paste your API Token into the `TOKEN` variable.
    * Add your User ID to the `ADMIN_IDS` list.

3.  **Install Dependencies**:
    * In your terminal, run: `pip install -r requirements.txt`

4.  **Run the Bot**:
    * In your terminal, run: `python3 bot.py`
    * The bot will print "Bot started..." and wait for your commands via Telegram.

## Commands
* `ls [path]`: Lists contents of a directory.
* `users`: Shows active users.
* `processes`: Shows running processes.
* `write [path] [data]`: Writes data to a file.
* `exec [command]`: Executes a shell command.
* `download [path]`: Downloads a file from the bot.
* `terminate`: Shuts down the bot.

## Security
This bot implements a mandatory authentication check based on user IDs. However, the `exec` command is powerful and inherently risky. Do not run this on a production system without further hardening and security reviews.

## Acknowledgments
This project was completed as part of academic coursework at **VIT Bhopal University** under the guidance of **Dr. N. D. Patel**.