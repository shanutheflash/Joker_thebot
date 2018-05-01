from FFbot.modules.sql.translation import prev_locale
from FFbot.modules.translations.German import GermanStrings
from FFbot.modules.translations.Dutch import DutchStrings
from FFbot.modules.translations.Indonesian import IndonesianStrings
from FFbot.modules.translations.Finnish import FinnishStrings

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
        elif LOCALE in ('fi') and t in FinnishStrings:
           return FinnishStrings[t]
        else:
           return t
    elif show_none:
        return t
