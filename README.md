# LeakCheck Discord Bot

A Discord bot that checks for data breaches using the LeakCheck API. The bot operates strictly via user DMs for privacy reasons. It sends detailed reports of any leaks found or confirms if no leaks were found. The bot also logs each command usage in the console.

## Setup

1. Clone this repository.
2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory of the project and add your Discord token and LeakCheck key:

    ```env
    DISCORD_TOKEN=your_discord_token
    LEAKCHECK_KEY=your_leakcheck_key
    ```

4. Run the bot:

    ```bash
    python index.py
    ```

## Usage

Send a DM to the bot with the `!leakcheck` command followed by an email:
!leakcheck email@example.com

The bot will reply with an embed containing the results of the leak check.
