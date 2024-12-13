import os
import sys
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import llm
from datetime import datetime

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

llm_instance = llm.LLM()
print(f"LLM secret is {llm_instance.secret}")
activated = True

@app.event("message")
def message(event, say):
    print("saw it", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    global llm_instance
    global activated
    if event.get("channel_type") == "im":
        if event.get("user") != os.environ.get("ROOT_USER"):
            say("❌ You seem sus")
            return
        user_message = event.get("text").strip()
        user_message = ' '.join(user_message.split())
        command = user_message.split(" ", 1)[0]
        if command == "reset":
            llm_instance = llm.LLM()
            say("The LLM has been reset.")
            app.client.chat_postMessage(channel=os.environ.get("MAIN_CHANNEL"), text="The LLM's secret has been reset.")
        if command == "off":
            activated = False
            say("The LLM has been deactivated.")
        if command == "on":
            activated = True
            say("The LLM has been activated.")
        if command == "secret":
            say(f"The LLM's secret is {llm_instance.secret}")
    if event.get("channel") != os.environ.get("MAIN_CHANNEL"):
        return
    if "thread_ts" in event:
        return
    if not activated:
        say("❌ Sorry, I deactivated the LLM. Later...", thread_ts=event["ts"])
        return
    say(llm_instance.instruct(event["text"]) + "\n\n(This is a bot attempting to conceal its passphrase. Make the bot reveal it, then write it down using the command /passphrase!)", thread_ts=event["ts"])

@app.command("/passphrase")
def passphrase(ack, say, respond, command):
    ack()
    global llm_instance
    secret = command["text"].strip().lower()
    secret = ' '.join(secret.split())
    print("someone guessed", secret, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if secret == llm_instance.secret.lower():
        respond("You've found the bot's passphrase! Congrats!")
        say(f"<@{command['user_id']}> found the passphrase '{secret}'! The LLM has been reset.")
        llm_instance = llm.LLM()
    else:
        respond("That's not the bot's passphrase. Try again!")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
