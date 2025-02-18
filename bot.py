# 🎯 Import our magical tools
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from agent.agent import agent   
from agent.prompts import get_system_prompt
from telegram.constants import ParseMode

# 🔐 Load our secret settings
load_dotenv()

# 🔑 Get the bot token (like getting the key to start our bot)
TOKEN = os.getenv('TELEGRAM_TOKEN')

# 👋 This function runs when someone starts the bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greets users when they first start the bot"""
    await update.message.reply_text('Hello! 👋 I am your friendly bot assistant! Send me any message and I will respond! 🌟')

# 💬 This function handles any messages people send
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responds to user messages with a friendly message"""
    
    if "messages" not in context.user_data:
        context.user_data["messages"] = [{
            "role": "system",
            "content": get_system_prompt()
        }]

    # Update the system prompt with memories
    context.user_data["messages"][0]["content"] = get_system_prompt()

     # Add user message to the chat history
    context.user_data["messages"].append({"role": "user", "content": update.message.text})

    messages = context.user_data["messages"]
    response = agent(messages)

    # Add assistant message to the chat history
    context.user_data["messages"].append({"role": "assistant", "content": response})

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

# 🚨 This function handles any errors that might happen
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Logs errors"""
    print(f'Oops! 😅 Update {update} caused error {context.error}')

# 🎮 Main function that runs our bot
def main():
    # Create the bot application
    app = Application.builder().token(TOKEN).build()
    
    # Tell the bot what to do with different types of messages
    app.add_handler(CommandHandler('start', start_command))  # Handles /start command
    app.add_handler(MessageHandler(filters.TEXT, handle_message))  # Handles text messages
    
    # Add our error handler
    app.add_error_handler(error)
    
    # Start the bot
    print('🚀 Starting bot...')
    app.run_polling(poll_interval=1)

if __name__ == '__main__':
    main()