# Defense LLM

Defense LLM is a Slack bot that uses a language model (LLM) to interact with users. The bot has a secret passphrase that users can try to guess. The bot can be activated, deactivated, and reset using specific commands.

## Features

- Responds to messages in Slack channels.
- Can be activated, deactivated, and reset.
- Users can try to guess the bot's secret passphrase.
- Uses OpenAI's GPT-4 model for generating responses.

## Setup

### Prerequisites

- Python 3.8 or higher
- Slack workspace and bot token
- OpenAI API key

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/khang200923/defense-llm
    cd defense-llm
    ```

2. Create a Slack app with this manifest:
    ```json
    {
        "display_information": {
            "name": "Defensive LLM"
        },
        "features": {
            "bot_user": {
                "display_name": "Defensive LLM",
                "always_online": false
            },
            "slash_commands": [
                {
                    "command": "/passphrase",
                    "description": "Checks whether the phrase is the correct passphrase for the Defensive LLM or not",
                    "usage_hint": "[phrase]",
                    "should_escape": false
                }
            ]
        },
        "oauth_config": {
            "scopes": {
                "bot": [
                    "channels:history",
                    "chat:write",
                    "commands",
                    "groups:history",
                    "im:read",
                    "im:history"
                ]
            }
        },
        "settings": {
            "event_subscriptions": {
                "bot_events": [
                    "message.channels",
                    "message.groups",
                    "message.im"
                ]
            },
            "interactivity": {
                "is_enabled": true
            },
            "org_deploy_enabled": false,
            "socket_mode_enabled": true,
            "token_rotation_enabled": false
        }
    }
    ```

3. Create an .env file:
    ```ini
    OPENAI_API_KEY=sk-proj-...
    SLACK_BOT_TOKEN=xoxb-...
    SLACK_APP_TOKEN=xapp-...
    MAIN_CHANNEL=C... # ID of the channel where this bot runs on
    ROOT_USER=U... # ID of the user controlling this bot
    ```

4. Run the app:
    ```bash
    python app.py
    ```

5. Have fun..?
    ![screenshot from the #defensive-llm channel](screenshot.png)

## Root User Commands

The root user can control the bot using the following commands in a direct message:

- `reset`: Resets the LLM and generates a new secret passphrase.
- `off`: Deactivates the LLM.
- `on`: Activates the LLM.
- `secret`: Reveals the current secret passphrase of the LLM.
