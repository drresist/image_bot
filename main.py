import os
import time
import urllib.request
import logging


from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
import telebot
from utils import show_exif, crop_image, extractCoordinates

admin = ""

# LOGGER
logging.basicConfig(filename='bot.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt = '%H:%M:%S',
                    level=logging.DEBUG)
logging.info("Running telebot log")
logger = telebot.logger
API_TOKEN = os.environ["IMAGE_BOT_API"]
bot = telebot.TeleBot(API_TOKEN)

# TODO: Add position tag and show on map
# Add already geo option. In utils had func for extrtacting geo, but not work correctly
# Add-24-09-2020: not all photo had geotag. Add error handling
BOT_OPTIONS = (" exif", " cropx2", " score", " geo")


# Handle images
@bot.message_handler(content_types=["document"])
def image_handler(message: telebot.types.Message):
    doc_name = "cache/" + message.document.file_name
    file =  bot.get_file(message.document.file_id)
    mime = message.document.mime_type.split("/")[0]
    if (
        mime == 'image'
        and message.chat.type == "private"
    ):
        # Send action Typing
        bot.send_chat_action(chat_id=message.chat.id, action="typing")
        # Download file
        url = ("https://api.telegram.org/file/bot"
                + API_TOKEN
                + "/" + file.file_path)
        urllib.request.urlretrieve(url, doc_name)
        # Send option actions with creation of new keyboard
        keyboard = InlineKeyboardMarkup()
        # add button + specify callback
        show_exif = InlineKeyboardButton(text="Show EXIF",
                                         callback_data=doc_name + BOT_OPTIONS[0])
        cropx2 = InlineKeyboardButton(text="Crop photo x2",
                                      callback_data=doc_name + BOT_OPTIONS[1])
        score = InlineKeyboardButton(text="Score",
                                     callback_data=doc_name + BOT_OPTIONS[2])
        geo = InlineKeyboardButton(text="Show on map",
                                   callback_data=doc_name + BOT_OPTIONS[3])
        # Create keyboard
        option_buttons = [show_exif, cropx2, score, geo]

        for k in option_buttons:
            keyboard.add(k)

        bot.reply_to(message,
                     text="Options:",
                     reply_markup=keyboard)

# Catch callback

# TODO: parse callback and add utils function - GEO map
# TODO: add function to delete images
# TODO: automatic remove files
# TODO: logging to txt file

@bot.callback_query_handler(func=lambda call: call.data.endswith(BOT_OPTIONS))
def parse_call(call: telebot.types.CallbackQuery):
    # define callback function
    func = call.data.split(' ')[-1]
    file = call.data.split(' ')[0]
    call_id = call.id
    if func == 'exif':
        try:
            print(show_exif(file))
            bot.answer_callback_query(
                callback_query_id=call.id,
                text=show_exif(file),
                show_alert=True
            )
        except Exception as e:
            print(e)
            bot.answer_callback_query(
                callback_query_id=call.id,
                text="Can't extract exif",
                show_alert=False
            )
    elif func == 'cropx2':
        # Use crop function
        cropped_image = crop_image(file)
        print(cropped_image)
        bot.send_document(
            chat_id=call.message.chat.id, data=open(f"{file}_cropx2.jpeg", "rb")
        )
    elif func == 'score':
        print("perform score calc's")
    elif func == 'geo':
        try:

            lat, longit = extractCoordinates(file)
            print(f"{lat} - {longit}")
        except:
            print("can't extract geo tag")


# Delete images by command #clean. Only access to admin acc

@bot.message_handler(regexp = "#clean")
def delete_images(message: telebot.types.Message):
    # if message.from_user in admin:
        cache = os.listdir("cache")
        for f in cache:
            os.remove("cache/"+f)
        print("Clean up complete")


# Run bot
bot.polling()
