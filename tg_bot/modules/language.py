from tg_bot.modules.sql.translation import switch_to_locale
from tg_bot.modules.translations.strings import tld
from telegram.ext import CommandHandler
from tg_bot import dispatcher

def change_locale(bot, update, args):
    chat = update.effective_chat
    if len(args) > 0:
        if args[0] in  ('English', 'German', 'French', 'Dutch'):
            switch_to_locale(chat.id, args[0])
            update.message.reply_text(tld(chat.id, 'Switched to {} Successfully!').format(args[0]))
        else:
            update.message.reply_text("{} not supported yet!".format(args[0]))

LOCALE_HANDLER = CommandHandler(["set_locale", "locale"], change_locale, pass_args=True)
dispatcher.add_handler(LOCALE_HANDLER)
