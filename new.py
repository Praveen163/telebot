from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
import telegram.ext.filters as filters
import asyncio

from data import Daata
from notice import fetch_notices

BOT_TOKEN = '7419700930:AAH2hGzvX3sFTaFhDxQGRhMlH0gkjULAp8c'

# Dictionary to store user IDs and their subscription status
subscribed_users = {}

async def result(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Enter your roll number:')

async def handle_message(update: Update, context: CallbackContext) -> None:
    roll_number = update.message.text.upper()
    result = find_record_by_roll(Daata, roll_number)
    table_data = [
        ["Sem I", result['s1'], result['cr1']],
        ["Sem 2", result['s2'], result['cr2']],
        ["Sem 3", result['s3'], result['cr3']],
        ["Sem 4", result['s4'], result['cr4']],
        ["Sem 5", result['s5'], result['cr5']],
        ["Sem 6", result['s6'], result['cr6']]
    ]

    if result:
        await update.message.reply_text("Sem ::: CGPA ::: Credits")
        for i in table_data:
            await update.message.reply_text(f"{i[0]} :  {i[1]} :  {i[2]}")
        
        weighted_sum = (result['s1'] * result['cr1'] +
                        result['s2'] * result['cr2'] +
                        result['s3'] * result['cr3'] +
                        result['s4'] * result['cr4'] +
                        result['s5'] * result['cr5'] +
                        result['s6'] * result['cr6'])
    
        total_credits = (result['cr1'] +
                         result['cr2'] +
                         result['cr3'] +
                         result['cr4'] +
                         result['cr5'] +
                         result['cr6'])
        cgpa = weighted_sum / total_credits
        await update.message.reply_text(f"Avg CGPA :  {cgpa:.2f}")
    
    else:
        await update.message.reply_text("Record not found.")

def find_record_by_roll(data, roll_number):
    for record in data:
        if record['roll'] == roll_number:
            return record
    return None

async def subscribe_notice(update: Update, context: CallbackContext) -> None:
    """Adds the user to the subscription list."""
    chat_id = update.effective_chat.id
    subscribed_users[chat_id] = True
    subscribed_users("sub : ",subscribed_users)
    await update.message.reply_text("You are now subscribed to notices.")

async def unsubscribe_notice(update: Update, context: CallbackContext) -> None:
    """Removes the user from the subscription list."""
    chat_id = update.effective_chat.id
    if chat_id in subscribed_users:
        del subscribed_users[chat_id]
        await update.message.reply_text("You are unsubscribed from notices.")
    else:
        await update.message.reply_text("You are not subscribed.")

async def check_notices(context: CallbackContext) -> None:
    """Fetches notices and sends them to all subscribed users."""
    print(subscribed_users)
    s = fetch_notices()
    if s:
        for chat_id in subscribed_users:
            try:
                await context.bot.send_message(chat_id=chat_id, text=s)
            except Exception as e:
                print(f"Failed to send notice to {chat_id}: {e}")

def main():
    # Initialize the application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers for subscribing/unsubscribing to notices
    application.add_handler(CommandHandler("result", result))
    application.add_handler(CommandHandler("subscribe", subscribe_notice))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe_notice))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Get the job queue from the application
    job_queue = application.job_queue
    
    # Set up a repeating job to check for notices every 600 seconds
    job_queue.run_repeating(check_notices, interval=600, first=10)  # first=10 to delay the first check slightly
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
