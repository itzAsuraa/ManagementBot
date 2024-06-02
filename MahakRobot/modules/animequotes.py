import json
import random
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from MahakRobot import dispatcher, OWNER_ID
from MahakRobot.modules.disable import DisableAbleCommandHandler

# Function to fetch a random anime quote
def anime_quote():
    url = "https://animechan.vercel.app/api/random"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        dic = response.json()  # Directly parse JSON response
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error fetching quote: {e}")
        return None, None, None  # Return None if there was an error

    quote = dic.get("quote")
    character = dic.get("character")
    anime = dic.get("anime")
    return quote, character, anime

# Command handler for /quote
def quotes(update: Update, context: CallbackContext):
    message = update.effective_message
    quote, character, anime = anime_quote()
    if quote and character and anime:  # Ensure we have valid data
        msg = f"<i>❝{quote}❞</i>\n\n<b>{character} from {anime}</b>"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Change", callback_data="change_quote")]])
        message.reply_text(msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        message.reply_text("Failed to fetch quote. Please try again later.", parse_mode=ParseMode.HTML)

# Callback query handler to change the quote
def change_quote(update: Update, context: CallbackContext):
    query = update.callback_query
    quote, character, anime = anime_quote()
    if quote and character and anime:  # Ensure we have valid data
        msg = f"<i>❝{quote}❞</i>\n\n<b>{character} from {anime}</b>"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Change", callback_data="change_quote")]])
        query.edit_message_text(msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        query.edit_message_text("Failed to fetch quote. Please try again later.", parse_mode=ParseMode.HTML)

# Command handler for /animequotes
def animequotes(update: Update, context: CallbackContext):
    message = update.effective_message
    quote_img = random.choice(QUOTES_IMG)
    reply_photo = message.reply_to_message.reply_photo if message.reply_to_message else message.reply_photo
    reply_photo(quote_img)

# List of anime quote images
QUOTES_IMG = [
    "https://i.imgur.com/Iub4RYj.jpg",
    "https://i.imgur.com/uvNMdIl.jpg",
    # Add more image URLs as needed
]

# Handlers
ANIMEQUOTES_HANDLER = DisableAbleCommandHandler("animequotes", animequotes)
QUOTES_HANDLER = DisableAbleCommandHandler("quote", quotes)
CHANGE_QUOTE_HANDLER = CallbackQueryHandler(change_quote, pattern=r"change_quote")

# Add handlers to the dispatcher
dispatcher.add_handler(ANIMEQUOTES_HANDLER)
dispatcher.add_handler(QUOTES_HANDLER)
dispatcher.add_handler(CHANGE_QUOTE_HANDLER)

__mod_name__ = "ǫᴜᴏᴛᴇ"
__help__ = """
❍ /quote ➛ ɢᴇᴛ ᴀ ʀᴀɴᴅᴏᴍ ᴀɴɪᴍᴇ ǫᴜᴏᴛᴇ.
❍ /animequotes ➛ ɢᴇᴛ ᴀ ʀᴀɴᴅᴏᴍ ᴀɴɪᴍᴇ ǫᴜᴏᴛᴇ ɪᴍᴀɢᴇ.
"""

__command_list__ = ["animequotes", "quote"]
__handlers__ = [ANIMEQUOTES_HANDLER, QUOTES_HANDLER, CHANGE_QUOTE_HANDLER]