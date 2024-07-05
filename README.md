# Screenshot to Discord Bot

This project is a Discord bot that monitors a specified directory for new screenshots and uploads them to a designated Discord channel. It uses the `watchdog` library to monitor file system events and the `discord.py` library to interact with Discord.

## Features

- Monitors a specified directory for new or modified screenshots.
- Uploads detected screenshots to a designated Discord channel.
- Uses debounce logic to ensure files are fully written before uploading.
- Handles errors gracefully and restarts the bot if necessary.

## Prerequisites

- Python 3.7 or higher
- Discord bot token
- `discord.py` library
- `watchdog` library

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/screenshot-to-discord-bot.git
    cd screenshot-to-discord-bot
    ```

2. **Install dependencies**:
    ```sh
    pip install discord watchdog
    ```

3. **Set up your environment**:
    - Replace `YOUR_DISCORD_BOT_TOKEN` with your actual Discord bot token.
    - Replace `YOUR_CHANNEL_ID` with the ID of the Discord channel where you want to upload the screenshots.

## Usage

1. **Run the bot**:
    ```sh
    python script.py
    ```

2. **Screenshots**:
    - The bot will monitor the specified directory (default is `'/Users/aarongurovich/Desktop'`).
    - When a new screenshot is created or modified in this directory, it will be uploaded to the designated Discord channel.

## Configuration

- **Directory to Monitor**:
  - By default, the script monitors `'Your Path'`. You can change this path by modifying the `screenshot_path` variable in the `main` function.
  
- **Discord Bot Token**:
  - Set your Discord bot token in the `TOKEN` variable.
  
- **Channel ID**:
  - Set the channel ID where the bot will upload screenshots in the `CHANNEL_ID` variable.

## Example

```python
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
CHANNEL_ID = 123456789012345678  # Replace with your Discord channel ID
screenshot_path = '/path/to/your/screenshots'
