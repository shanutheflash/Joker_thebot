from tg_bot.modules.sql.translation import prev_locale
from tg_bot.modules.translations.German import GermanStrings
from tg_bot.modules.translations.Dutch import DutchStrings
from tg_bot.modules.translations.Indonesian import IndonesianStrings

def tld(chat_id, t, show_none=True):
    LANGUAGE = prev_locale(chat_id)
    if LANGUAGE:
        LOCALE = LANGUAGE.locale_name
        if LOCALE in ('nl') and t in DutchStrings:
            return DutchStrings[t]
        elif LOCALE in ('de') and t in GermanStrings:
           return GermanStrings[t]
        elif LOCALE in ('id') and t in IndonesianStrings:
           return IndonesianStrings[t]
        else:
           return t
    elif show_none:
        return t
