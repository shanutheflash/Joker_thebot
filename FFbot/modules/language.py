from FFbot.modules.sql.translation import switch_to_locale
from FFbot.modules.translations.strings import tld
from telegram.ext import CommandHandler
from FFbot import dispatcher
from FFbot.modules.translations.list_locale import list_locales

def change_locale(bot, update, args):
    chat = update.effective_chat
    if len(args) > 0:
        locale = args[0].lower()
        if locale in list_locales:
            if locale in  ('en', 'de', 'nl', 'id', 'fi'):
                switch_to_locale(chat.id, locale)
                update.message.reply_text(tld(chat.id, 'Switched to {} successfully!').format(list_locales[locale]))
            else:
                update.message.reply_text("{} not supported yet!".format(list_locales[locale]))
        else:
            update.message.reply_text("Is this even a language?")
    else:
        update.message.reply_text("You haven't give me a locale to begin with!")

LOCALE_HANDLER = CommandHandler(["set_locale", "locale"], change_locale, pass_args=True)
dispatcher.add_handler(LOCALE_HANDLER)
