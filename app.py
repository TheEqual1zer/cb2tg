from telegram.ext import *
from telegram import *
from credentials import *
from locales import *
from magic import *
from datetime import *

# Used:
# https://docs.python-telegram-bot.org/en/stable/
# https://docs.python.org/3/library/xml.etree.elementtree.html
# https://docs.python-requests.org/en/latest/
# https://docs.python.org/3/tutorial/datastructures.html


class Menu(InlineKeyboardMarkup):
    def __init__(self, date=date.today().strftime("%d/%m/%Y")):
        super().__init__([[InlineKeyboardButton(a[1][1], callback_data=f"{a[0]}_{date}") for a in cur_list.items()
                           if getrates(f"{a[0]}_{date}")]])


def start(update: Update, context: CallbackContext):
    buttons = [[InlineKeyboardButton("🇷🇺", callback_data="ru")],
               [InlineKeyboardButton("🇬🇧", callback_data="en")]]
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("resources/globe.png", "rb"),
                           reply_markup=InlineKeyboardMarkup(buttons))


def language_selected(user, lang):
    user.send_message(f"<i>{phrases['language'][lang]}</i>", parse_mode=ParseMode.HTML)
    buttons = [[KeyboardButton(phrases["menu_current"][lang])], [KeyboardButton(phrases["menu_date"][lang])]]
    user.send_message(phrases["main_menu"][lang], reply_markup=ReplyKeyboardMarkup(buttons))


def messagehandler(update: Update, context: CallbackContext):
    msg = update.message.text
    lang = "".join([list(k[1].keys())[list(k[1].values()).index(msg)] for k in phrases.items() if msg in k[1].values()])
    # if current rates button is pressed
    if msg in phrases["menu_current"].values():
        update.message.reply_text("💸", reply_markup=Menu())
    # if rates for date is pressed
    if msg in phrases["menu_date"].values():
        update.message.reply_text(f'{phrases["menu_date_prompt"][lang]}:', parse_mode=ParseMode.HTML)
    # if date is entered
    if msg.count(".") == 2:
        update.message.reply_text("💸", reply_markup=Menu(datetime.strptime(msg, "%d.%m.%Y").strftime("%d/%m/%Y")))


def queryhandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()
    if query in locales:
        language_selected(update.callback_query.from_user, query)
    else:
        update.callback_query.from_user.send_message(getrates(query))


def error(update, context):
    update.message.reply_text('an error occured')


def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(queryhandler))
    dispatcher.add_handler(MessageHandler(Filters.text, messagehandler))
    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
