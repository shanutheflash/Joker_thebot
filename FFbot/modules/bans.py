import html
import time
from typing import Optional, List
from FFbot.modules.translations.strings import tld
from telegram import Message, Chat, Update, Bot, User
from telegram.error import BadRequest
from telegram.ext import run_async, CommandHandler, Filters
from telegram.utils.helpers import mention_html

from FFbot import dispatcher, BAN_STICKER, LOGGER
from FFbot.modules.disable import DisableAbleCommandHandler
from FFbot.modules.helper_funcs.chat_status import bot_admin, user_admin, is_user_ban_protected, can_restrict, \
    is_user_admin, is_user_in_chat
from FFbot.modules.helper_funcs.extraction import extract_user_and_text
from FFbot.modules.log_channel import loggable
from FFbot.modules.helper_funcs.filters import CustomFilters

@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def ban(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(tld(chat.id, "You don't seem to be referring to a user."))
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text(tld(chat.id, "I can't seem to find this user"))
            return ""
        else:
            raise

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text(tld(chat.id, "I really wish I could ban admins..."))
        return ""

    if user_id == bot.id:
        update.effective_message.reply_text(tld(chat.id, "I'm not gonna BAN myself, are you crazy?"))
        return ""

    log = "<b>{}:</b>" \
          "\n#BANNED" \
          "\n<b>Admin:</b> {}" \
          "\n<b>User:</b> {}".format(html.escape(chat.title), mention_html(user.id, user.first_name),
                                     mention_html(member.user.id, member.user.first_name))
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    try:
        update.effective_chat.kick_member(user_id)
        bot.send_sticker(update.effective_chat.id, BAN_STICKER)  # banhammer marie sticker
        message.reply_text(tld(chat.id, "Banned!"))
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text('Banned!', quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR banning user %s in chat %s (%s) due to %s", user_id, chat.title, chat.id,
                             excp.message)
            message.reply_text(tld(chat.id, "Well damn, I can't ban that user."))

    return ""


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def temp_ban(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(tld(chat.id, "You don't seem to be referring to a user."))
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text(tld(chat.id, "I can't seem to find this user"))
            return ""
        else:
            raise

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text(tld(chat.id, "I really wish I could ban admins..."))
        return ""

    if user_id == bot.id:
        update.effective_message.reply_text(tld(chat.id, "I'm not gonna BAN myself, are you crazy?"))
        return ""

    split_reason = reason.split(None, 1)
    if not reason:
        message.reply_text(tld(chat.id, "You haven't specified a time to ban this user for!"))
        return ""

    else:
        time_val = split_reason[0].lower()
        if len(split_reason) > 1:
            reason = split_reason[1]
        else:
            reason = ""

    if any(time_val.endswith(unit) for unit in ('m', 'h', 'd')):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            message.reply_text(tld(chat.id, "Invalid time amount specified."))
            return ""

        if unit == 'm':
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == 'h':
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == 'd':
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        else:
            # how even...?
            return ""

    else:
        message.reply_text(tld(chat.id, "Invalid time type specified. Expected m,h, or d, got: {}").format(time_val[-1]))
        return ""

    log = "<b>{}:</b>" \
          "\n#TEMP BANNED" \
          "\n<b>Admin:</b> {}" \
          "\n<b>User:</b> {}" \
          "\n<b>Time:</b> {}".format(html.escape(chat.title), mention_html(user.id, user.first_name),
                                     mention_html(member.user.id, member.user.first_name), time_val)
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    try:
        update.effective_chat.kick_member(user_id, until_date=bantime)
        bot.send_sticker(update.effective_chat.id, BAN_STICKER)  # banhammer marie sticker
        message.reply_text(tld(chat.id, "Banned! User will be banned for {}.").format(time_val))
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(tld(chat.id, "Banned!User will be banned for {}.").format(time_val), quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR banning user %s in chat %s (%s) due to %s", user_id, chat.title, chat.id,
                             excp.message)
            message.reply_text(tld(chat.id, "Well damn, I can't ban that user."))

    return ""


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def kick(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text(tld(chat.id, "I can't seem to find this user"))
            return ""
        else:
            raise

    if is_user_ban_protected(chat, user_id):
        message.reply_text(tld(chat.id, "I really wish I could kick admins..."))
        return ""

    if user_id == bot.id:
        update.effective_message.reply_text(tld(chat.id, "Yeahhh I'm not gonna do that"))
        return ""

    res = update.effective_chat.unban_member(user_id)  # unban on current user = kick
    if res:
        bot.send_sticker(update.effective_chat.id, BAN_STICKER)  # banhammer marie sticker
        message.reply_text(tld(chat.id, "Kicked!"))
        log = "<b>{}:</b>" \
              "\n#KICKED" \
              "\n<b>Admin:</b> {}" \
              "\n<b>User:</b> {}".format(html.escape(chat.title),
                                         mention_html(user.id, user.first_name),
                                         mention_html(member.user.id, member.user.first_name))
        if reason:
            log += "\n<b>Reason:</b> {}".format(reason)

        return log

    else:
        message.reply_text(tld(chat.id, "Well damn, I can't kick that user."))

    return ""


@run_async
@bot_admin
@can_restrict
def kickme(bot: Bot, update: Update):
    user_id = update.effective_message.from_user.id
    chat = update.effective_chat

    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text(tld(chat.id, "I wish I could... but you're an admin."))
        return

    res = update.effective_chat.unban_member(user_id)  # unban on current user = kick
    if res:
        update.effective_message.reply_text(tld(chat.id, "Get out from here."))
    else:
        update.effective_message.reply_text(tld(chat.id, "Huh? I can't :/"))


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def unban(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message  # type: Optional[Message]
    user = update.effective_user  # type: Optional[User]
    chat = update.effective_chat  # type: Optional[Chat]

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text(tld(chat.id, "I can't seem to find this user"))
            return ""
        else:
            raise

    if user_id == bot.id:
        update.effective_message.reply_text(tld(chat.id, "How would I unban myself if I wasn't here...?"))
        return ""

    if is_user_in_chat(chat, user_id):
        update.effective_message.reply_text(tld(chat.id, "Why are you trying to unban someone that's already in the chat?"))
        return ""

    update.effective_chat.unban_member(user_id)
    message.reply_text(tld(chat.id, "Yep, this user can join!"))

    log = "<b>{}:</b>" \
          "\n#UNBANNED" \
          "\n<b>Admin:</b> {}" \
          "\n<b>User:</b> {}".format(html.escape(chat.title),
                                     mention_html(user.id, user.first_name),
                                     mention_html(member.user.id, member.user.first_name))
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    return log


@run_async
@bot_admin
def rban(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message

    if not args:
        message.reply_text(tld(chat.id, "You don't seem to be referring to a chat/user."))
        return

    user_id, chat_id = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(tld(chat.id, "You don't seem to be referring to a user."))
        return
    elif not chat_id:
        message.reply_text(tld(chat.id, "You don't seem to be referring to a chat."))
        return

    try:
        chat = bot.get_chat(chat_id)
    except BadRequest as excp:
        if excp.message == "Chat not found":
            message.reply_text(tld(chat.id, "Chat not found! Make sure you entered a valid chat ID and I'm part of that chat."))
            return
        else:
            raise

    if chat.type == 'private':
        message.reply_text(tld(chat.id, "I'm sorry, but that's a private chat!"))
        return

    if not is_bot_admin(chat, bot.id) and not chat.get_member(bot.id).can_restrict_members:
        message.reply_text(tld(chat.id, "I can't restrict people there! Make sure I'm admin and can ban users."))
        return

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text(tld(chat.id, "I can't seem to find this user"))
            return
        else:
            raise

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text(tld(chat.id, "I really wish I could ban admins..."))
        return

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "I'm not gonna BAN myself, are you crazy?"))
        return

    try:
        chat.kick_member(user_id)
        message.reply_text(tld(chat.id, "Banned!"))
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text('Banned!', quote=False)
        elif excp.message == "User_not_participant":
            message.reply_text("This user is not a participant of the chat!")
        elif excp.message == "Group chat was deactivated":
            message.reply_text("This group chat was deactivated!")
        elif excp.message == "Need to be inviter of a user to kick it from a basic group":
            message.reply_text(excp.message)
        elif excp.message == "Only the creator of a basic group can kick group administrators":
            message.reply_text(excp.message)
        elif excp.message == "Peer_id_invalid":
            message.reply_text("Could not ban user. Perhaps the group has been suspended by Telegram.")
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR banning user %s in chat %s (%s) due to %s", user_id, chat.title, chat.id,
                             excp.message)
            message.reply_text("Well damn, I can't ban that user.")


__help__ = """
 - /kickme: kicks the user who issued the command

*Admin only:*
 - /ban <userhandle>: bans a user. (via handle, or reply)
 - /tban <userhandle> x(m/h/d): bans a user for x time. (via handle, or reply). m = minutes, h = hours, d = days.
 - /unban <userhandle>: unbans a user. (via handle, or reply)
 - /kick <userhandle>: kicks a user, (via handle, or reply)
"""

__mod_name__ = "Bans"

BAN_HANDLER = CommandHandler("ban", ban, pass_args=True, filters=Filters.group)
TEMPBAN_HANDLER = CommandHandler(["tban", "tempban"], temp_ban, pass_args=True, filters=Filters.group)
KICK_HANDLER = CommandHandler("kick", kick, pass_args=True, filters=Filters.group)
UNBAN_HANDLER = CommandHandler("unban", unban, pass_args=True, filters=Filters.group)
KICKME_HANDLER = DisableAbleCommandHandler("kickme", kickme, filters=Filters.group)
RBAN_HANDLER = CommandHandler("rban", rban, pass_args=True, filters=CustomFilters.sudo_filter)

dispatcher.add_handler(BAN_HANDLER)
dispatcher.add_handler(TEMPBAN_HANDLER)
dispatcher.add_handler(KICK_HANDLER)
dispatcher.add_handler(UNBAN_HANDLER)
dispatcher.add_handler(KICKME_HANDLER)
dispatcher.add_handler(RBAN_HANDLER)
