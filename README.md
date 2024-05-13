"# SNA Welcome Bot

## Overview
This repository contains the code for a Telegram bot designed to welcome new members to a group chat. The bot is built using the `telebot` library and integrates with a Flask web application to handle webhook events.

**********
README file for botfunctions.py

## Features
- Welcomes new members to the Telegram group with a custom message.
- Provides a deep link for new members to access a welcome kit.
- Handles the `/start` command to trigger specific actions within the group.
- Stores user details in a database using the `Userbase` class from `dbfunctions`.

## Configuration
The bot uses a `config.json` file to manage configurations such as the bot token and webhook URL. Ensure that you have set the correct configuration file path in the `get_config` function.

## Installation
To set up the bot, follow these steps:
1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up your `config.json` file with the necessary bot token and webhook URL.
4. Run the Flask application with `python botfunctions.py`.

## Usage
Once the bot is running, it will automatically respond to new members joining the group and to commands sent by users.

## Acknowledgments
- telebot - The Python library used to interface with the Telegram Bot API.
- Flask - The web framework used for handling webhook events.

************
README file for dbfunctions.py

## dbfunctions.py

This module handles the database operations for the SNA Welcome Bot. It uses MongoDB as the backend database to store and manage user details.

### Features
- Connects to a MongoDB instance using a connection string from the `config.json` file.
- Provides functions to add and update user details in the database.
- Retrieves the latest group information associated with a user.
- Marks users as triggered when certain conditions are met.

### Configuration
Ensure that the MongoDB connection string is correctly set in the `config.json` file. The `get_config` function is used to retrieve configuration values.

### Usage
The `Userbase` class provides methods to interact with the database:
- `add_user_details`: Adds a new user's details to the database or updates existing information.
- `get_group_id`: Retrieves the last updated group name for a given username.
- `update_if_triggered`: Marks a user as triggered in the database.
- `update_only_in_group`: Updates the user's group information in the database.

### Dependencies
- pymongo: A Python driver for MongoDB. Install it using `pip install pymongo`.

### Setup
1. Ensure that MongoDB is installed and running on your server.
2. Update the `config.json` file with the correct MongoDB connection string.
3. Use the methods provided by the `Userbase` class to perform database operations as needed.

*****************
README file for your config.json

## Configuration

The `config.json` file contains the necessary configuration for the SNA Welcome Bot. It includes the bot token, webhook URL, file paths for messages and documents, and group IDs for the Telegram groups.

### Structure
The configuration file is a JSON object with the following keys:
- `bot_token`: The token provided by BotFather for your Telegram bot.
- `username`: The username of your bot on Telegram.
- `mongodb_connection_string`: The connection string for your MongoDB instance.
- `sop_file_path`: The file path to the Standard Operating Procedure document.
- `thumbnail`: The file path to the thumbnail image used in messages.
- `welcome_message`: The file path to the welcome message template.
- `general_message`: The file path to the general message template.
- `webhook_url`: The URL to which Telegram will send updates.
- `group_id`: An object mapping group IDs to their respective names.

### Updating Configuration
To update the bot's configuration, modify the `config.json` file with the new values and restart the bot for the changes to take effect.

*************************

README file for: How to include the hosting setup and Apache2 configuration commands

# Hosting Setup and Apache2 Configuration

## Prerequisites
Before proceeding with the setup, ensure that you have Apache2 installed on your server. You will also need `sudo` privileges to execute the configuration commands.

## Steps to Host the Bot

1. **Switch to Superuser Mode**
   To perform administrative tasks, switch to superuser mode:
   ```bash
   sudo su -
   ```

2. **Stop Apache2 Service**
   Stop the currently running Apache2 service to apply new configurations:
   ```bash
   source /etc/apache2/envvars
   apache2 -k stop
   ```
   or

   ```bash
   service apache2 stop
   ```

3. **Configure Apache2 Virtual Host**
   Edit the Apache2 virtual host configuration file. You can use nano or vim to edit the file:
   ```bash
   nano /home/vishalsv2002/htconfig/000-default.conf
   ```

4. Add the following configuration to the file:
   ```apacheconf
   <VirtualHost *:80>
       ServerName vishalsv.selfmade.one
       ServerAdmin vishalsv2002@essentials
       WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
       <Directory /var/www/FlaskApp/FlaskApp/>
           Order allow,deny
           Allow from all
       </Directory>
       Alias /static /var/www/FlaskApp/FlaskApp/static
       <Directory /var/www/FlaskApp/FlaskApp/static/>
           Order allow,deny
           Allow from all
       </Directory>
       ErrorLog ${APACHE_LOG_DIR}/error.log
       LogLevel warn
       CustomLog ${APACHE_LOG_DIR}/access.log combined
   </VirtualHost>
   ```

5. **Create the WSGI File**
   Create a WSGI file that will serve as the entry point for the Flask application:
   ```bash
   nano /var/www/FlaskApp/flaskapp.wsgi
   ```

6. Add the following content to the flaskapp.wsgi file:
   ```python
   import sys
   import logging
   logging.basicConfig(stream=sys.stderr)
   sys.path.insert(0,"/home/vishalsv2002/telegram_sna_welcome_bot")

   from botfunctions import app as application
   ```

7. **Start Apache2 Service**
   After saving the changes, start the Apache2 service:
   ```bash
   apache2 -k start
   ```
   or

   ```bash
   service apache2 start
   ```

# Notes
- Replace `/home/vishalsv2002/telegram_sna_welcome_bot` with the actual path to your bot’s directory.
- Ensure that the `ServerName` matches your domain name.
- The `ServerAdmin` should be your email address or another identifier for the server administrator.
- Adjust the paths under `WSGIScriptAlias`, `Directory`, and `Alias` to match your server’s directory structure.

# Troubleshooting
If you encounter any issues, check the Apache error logs for more information:
```bash
cat ${APACHE_LOG_DIR}/error.log
```

# For further assistance, please refer to the Apache documentation or open an issue in this repository."

