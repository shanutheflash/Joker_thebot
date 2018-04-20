from tg_bot.modules.sql.translation import prev_locale

GermanStrings = {'Muted!' : 'Stummgeschalte!' ,
                 'Switched to {} Successfully!' : 'Erfolgreich auf {} geschaltet!'}

DutchStrings = { 'Switched to {} Successfully!' : 'Succesvol naar {} gewisseld!'}

def tld(chat_id, t):
    LANGUAGE = prev_locale(chat_id)
    if LANGUAGE == 'German' and t in GermanStrings:
        return GermanStrings[t]
    else:
        return t
    if LANGUAGE == 'Dutch' and t in DutchStrings:
        return DutchStrings[t]
    else:
       return t
