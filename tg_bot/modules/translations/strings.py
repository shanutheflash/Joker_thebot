from tg_bot.modules.sql.translation import prev_locale
from tg_bot.modules.translations.German import GermanStrings
from tg_bot.modules.translations.Dutch import DutchStrings

def tld(chat_id, t):
    LANGUAGE = prev_locale(chat_id)
    if LANGUAGE in ('dutch', 'nederland') and t in DutchStrings:
        return DutchStrings[t]
    elif LANGUAGE == 'german' and t in GermanStrings:
        return GermanStrings[t]
    else:
        return t
