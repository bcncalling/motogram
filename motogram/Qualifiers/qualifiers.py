#motogram: An asynchronous Python wrapper for the Telegram Bot API.
#
#This library is based on pyrogram (https://github.com/pyrogram/pyrogram).
#Copyright (C) 2023 [Santhu]
#
#motogram is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#motogram is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with motogram.  If not, see <https://www.gnu.org/licenses/>.

import inspect
import re
from typing import Callable, Union, List, Pattern

import motogram
from motogram import checks
from motogram.types import Chat, BackQuery, Inline, InlineButtonMarkup, ReplyButtonMarkup

class Qualifier:
    def __invert__(self):
        return InvertQualifier(self)

    def __and__(self, other):
        return AndQualifier(self, other)

    def __or__(self, other):
        return OrQualifier(self, other)


class InvertQualifier(Qualifier):
    def __init__(self, base):
        self.base = base

    async def __call__(self, mtclient: "motogram.MotoClient", chat: Chat):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(mtclient, chat)
        else:
            x = await mtclient.loop.run_in_executor(
                mtclient.executor,
                self.base,
                mtclient, chat
            )

        return not x


class AndQualifier(Qualifier):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, mtclient: "motogram.MotoClient", chat: Chat):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(mtclient, chat)
        else:
            x = await mtclient.loop.run_in_executor(
                mtclient.executor,
                self.base,
                mtclient, chat
            )

        # short circuit
        if not x:
            return False

        if inspect.iscoroutinefunction(self.other.__call__):
            y = await self.other(mtclient, chat)
        else:
            y = await mtclient.loop.run_in_executor(
                mtclient.executor,
                self.other,
                mtclient, chat
            )

        return x and y


class OrQualifier(Qualifier):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, mtclient: "motogram.MotoClient", chat: Chat):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(mtclient, chat)
        else:
            x = await mtclient.loop.run_in_executor(
                mtclient.executor,
                self.base,
                mtclient, chat
            )

        # short circuit
        if x:
            return True

        if inspect.iscoroutinefunction(self.other.__call__):
            y = await self.other(mtclient, chat)
        else:
            y = await mtclient.loop.run_in_executor(
                mtclient.executor,
                self.other,
                mtclient, chat
            )

        return x or y


CUSTOM_QUALIFIER_NAME = "CustomQualifier"

def create(func: Callable, name: str = None, **kwargs) -> Qualifier:
    return type(
        name or func.__name__ or CUSTOM_QUALIFIER_NAME,
        (Qualifier,),
        {"__call__": func, **kwargs}
    )()


async def all_qualifier(_, __, ___):
    return True

all = create(all_qualifier)

async def me_qualifier(_, __, chat: Chat):
    return bool(chat.from_user and chat.from_user.is_self or getattr(chat, "outgoing", False))
  
me = create(me_qualifier)

async def bot_qualifier(_, __, chat: Chat):
    return bool(chat.from_user and chat.from_user.is_bot)

bot = create(bot_qualifier)

async def app_qualifier(_, __, chat: Chat):
    return bool(chat.from_user)

app = create(app_qualifier)

async def dev_qualifier(_, __, chat: types.Chat):
    """
    Qualifier function to check if the message is from a user.
    """
    return bool(chat.from_user)

dev = create(dev_qualifier)

async def income_qualifier(_, __, chat: Chat):
    return not chat.income

income = create(income_qualifier)

async def out_qualifier(_, __, chat: Chat):
    return chat.out

out = create(out_qualifier)

async def text_qualifier(_, __, chat: Chat):
    return bool(chat.text)

text = create(text_qualifier)

async def reply_qualifier(_, __, chat: Chat):
    return bool(chat.reply_to_message_id)

reply = create(reply_qualifier)

async def forwarded_qualifier(_, __, chat: Chat):
    return bool(chat.forward_date)

forwarded = create(forwarded_qualifier)

async def caption_qualifier(_, __, chat: Chat):
    return bool(chat.caption)

caption = create(caption_qualifier)

async def audio_qualifier(_, __, chat: Chat):
    return bool(chat.audio)

audio = create(audio_qualifier)

async def doc_qualifier(_, __, chat: Chat):
    return bool(chat.doc)

doc = create(doc_qualifier)

async def photo_qualifier(_, __, chat: Chat):
    return bool(chat.photo)

photo = create(photo_qualifier)

async def stick_qualifier(_, __, chat: Chat):
    return bool(chat.stick)

stick = create(stick_qualifier)

async def animation_qualifier(_, __, chat: Chat):
    return bool(chat.animation)

animation = create(animation_qualifier)

async def game_qualifier(_, __, chat: Chat):
    return bool(chat.game)

game = create(game_qualifier)

async def video_qualifier(_, __, chat: Chat):
    return bool(chat.video)

video = create(video_qualifier)

async def media_group_qualifier(_, __, chat: Chat):
    return bool(chat.media_group_id)

media_group = create(media_group_qualifier)

async def voice_qualifier(_, __, chat: Chat):
    return bool(chat.voice)

voice = create(voice_qualifier)

async def video_note_qualifier(_, __, chat: Chat):
    return bool(chat.video_note)

video_note = create(video_note_qualifier)

async def contact_qualifier(_, __, chat: Chat):
    return bool(chat.contact)

contact = create(contact_qualifier)

async def location_qualifier(_, __, chat: Chat):
    return bool(chat.location)

location = create(location_qualifier)

async def venue_qualifier(_, __, chat: Chat):
    return bool(chat.venue)

venue = create(venue_qualifier)

async def web_page_qualifier(_, __, chat: Chat):
    return bool(chat.web_page)

web_page = create(web_page_qualifier)

async def poll_qualifier(_, __, chat: Chat):
    return bool(chat.poll)

poll = create(poll_qualifier)

async def dice_qualifier(_, __, chat: Chat):
    return bool(chat.dice)

dice = create(dice_qualifier)

async def media_spoiler_qualifier(_, __, chat: Chat):
    return bool(chat.has_media_spoiler)

media_spoiler = create(media_spoiler_qualifier)

async def pvt_qualifier(_, __, chat: Chat):
    return bool(chat and chat.type in {checks.ChatType.PRIVATE, checks.ChatType.BOT})

pvt = create(pvt_qualifier)

async def grp_qualifier(_, __, chat: Chat):
    return bool(chat and chat.type in {checks.ChatType.GROUP, checks.ChatType.SUPERGROUP})

grp = create(grp_qualifier)

async def chnl_qualifier(_, __, chat: Chat):
    return bool(chat and chat.type == checks.ChatType.CHANNEL)

chnl = create(chnl_qualifier)

async def new_chat_account_qualifier(_, __, chat: Chat):
    return bool(chat.new_chat_account)

new_chat_account = create(new_chat_account_qualifier)

async def left_chat_account_qualifier(_, __, chat: Chat):
    return bool(chat.left_chat_account)

left_chat_account = create(left_chat_account_qualifier)

async def new_chat_title_qualifier(_, __, chat: Chat):
    return bool(chat.new_chat_title)

new_chat_title = create(new_chat_title_qualifier)

async def new_chat_photo_qualifier(_, __, chat: Chat):
    return bool(chat.new_chat_photo)

new_chat_photo = create(new_chat_photo_qualifier)

async def delete_chat_photo_qualifier(_, __, chat: Chat):
    return bool(chat.delete_chat_photo)

delete_chat_photo = create(delete_chat_photo_qualifier)

async def group_chat_created_qualifier(_, __, chat: Chat):
    return bool(chat.group_chat_created)

group_chat_created = create(group_chat_created_qualifier)

async def supergroup_created_qualifier(_, __, chat: Chat):
    return bool(chat.supergroup_created)

supergroup_created = create(supergroup_created_qualifier)

async def channel_chat_created_qualifier(_, __, chat: Chat):
    return bool(chat.channel_chat_created)

channel_chat_created = create(channel_chat_created_qualifier)

async def migrate_to_chat_id_qualifier(_, __, chat: Chat):
    return bool(chat.migrate_to_chat_id)

migrate_to_chat_id = create(migrate_to_chat_id_qualifier)

async def migrate_from_chat_id_qualifier(_, __, chat: Chat):
    return bool(chat.migrate_from_chat_id)

migrate_from_chat_id = create(migrate_from_chat_id_qualifier)

async def pinned_message_qualifier(_, __, chat: Chat):
    return bool(chat.pinned_message)

pinned_message = create(pinned_message_qualifier)

async def game_high_score_qualifier(_, __, chat: Chat):
    return bool(chat.game_high_score)

game_high_score = create(game_high_score_qualifier)

async def reply_keyboard_qualifier(_, __, chat: Chat):
    return isinstance(chat.reply_markup, ReplyKeyboardMarkup)

reply_keyboard = create(reply_keyboard_qualifier)

async def inline_keyboard_qualifier(_, __, chat: Chat):
    return isinstance(chat.reply_markup, InlineKeyboardMarkup)

inline_keyboard = create(inline_keyboard_qualifier)

async def mentioned_qualifier(_, __, chat: Chat):
    return bool(chat.mentioned)

mentioned = create(mentioned_qualifier)

async def via_bot_qualifier(_, __, chat: Chat):
    return bool(chat.via_bot)

via_bot = create(via_bot_qualifier)

async def video_chat_started_qualifier(_, __, chat: Chat):
    return bool(chat.video_chat_started)

video_chat_started = create(video_chat_started_qualifier)

async def vc_chat_ended_qualifier(_, __, chat: Chat):
    return bool(chat.vc_chat_ended)

vc_chat_ended = create(vc_chat_ended_qualifier)

async def vc_members_invited_qualifier(_, __, chat: Chat):
    return bool(chat.vc_members_invited)

vc_members_invited = create(vc_members_invited_qualifier)

async def service_qualifier(_, __, chat: Chat):
    return bool(chat.service)

service = create(service_qualifier)

async def media_qualifier(_, __, chat: Chat):
    return bool(chat.media)

media = create(media_qualifier)

async def scheduled_qualifier(_, __, chat: Chat):
    return bool(chat.scheduled)

scheduled = create(scheduled_qualifier)

async def from_scheduled_qualifier(_, __, chat: Chat):
    return bool(chat.from_scheduled)

from_scheduled = create(from_scheduled_qualifier)

async def linked_channel_qualifier(_, __, chat: Chat):
    return bool(chat.forward_from_chat and not chat.from_user)

linked_channel = create(linked_channel_qualifier)

def enact(enact: Union[str, List[str]], prefixes: Union[str, List[str]] = "/", case_sensitive: bool = False):
    """Qualifier commands, i.e.: text messages starting with "/" or any other custom prefix.
    Parameters:
        enacts (``str`` | ``list``):
            The enact or list of enact as string the filter should look for.
            Examples: "start", ["start", "help", "settings"]. When a message text containing
            a enact arrives, the enact itself and its arguments will be stored in the *enact*
            field of the :obj:`~motogram.types.Chat`.

        prefixes (``str`` | ``list``, *optional*):
            A prefix or a list of prefixes as string the filter should look for.
            Defaults to "/" (slash). Examples: ".", "!", ["/", "!", "."], list(".:!").
            Pass None or "" (empty string) to allow enacts with no prefix at all.

        case_sensitive (``bool``, *optional*):
            Pass True if you want your enact(s) to be case sensitive. Defaults to False.
            Examples: when True, enact="Start" would trigger /Start but not /start.
    """
    enacts_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

    async def func(flt, mtclient: motogram.MotoClient, chat: Chat):
        username = mtclient.me.username or ""
        text = chat.text or chat.caption
        chat.enact = None

        if not text:
            return False

        for prefix in flt.prefixes:
            if not text.startswith(prefix):
                continue

            without_prefix = text[len(prefix):]

            for cmd in flt.enacts:
                if not re.match(rf"^(?:{cmd}(?:@?{username})?)(?:\s|$)", without_prefix,
                                flags=re.IGNORECASE if not flt.case_sensitive else 0):
                    continue

                without_enact = re.sub(rf"{cmd}(?:@?{username})?\s?", "", without_prefix, count=1,
                                         flags=re.IGNORECASE if not flt.case_sensitive else 0)

                chat.enact = [cmd] + [
                    re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                    for m in command_re.finditer(without_enact)
                ]

                return True

        return False

    enacts = enacts if isinstance(enacts, list) else [enacts]
    enacts = {c if case_sensitive else c.lower() for c in enacts}

    prefixes = [] if prefixes is None else prefixes
    prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
    prefixes = set(prefixes) if prefixes else {""}

    return create(
        func,
        "EnactQualifier",
        enacts=enacts,
        prefixes=prefixes,
        case_sensitive=case_sensitive
    )

class Event:
    async def __call__(self, mtclient: "motogram.MotoClient", chat: Chat = None, back_query: BackQuery = None, inline: Inline = None):
        if chat:
            value = chat.text or chat.caption
        elif callback_query:
            value = back_query.data
        elif inline_query:
            value = inline.query
        else:
            raise ValueError("Event filter requires either a chat, back_query, or inline parameter")

        if value:
            self.matches = list(self.pattern.finditer(value)) or None

        return bool(self.matches)

    def __init__(self, pattern: Union[str, Pattern], flags: int = 0):
        self.pattern = pattern if isinstance(pattern, Pattern) else re.compile(pattern, flags)

    def __invert__(self):
        return InvertQualifier(self)


class User(Qualifier, set):
    def __init__(self, users: Union[int, str, List[Union[int, str]]] = None):
        users = [] if users is None else users if isinstance(users, list) else [users]

        super().__init__(
            "me" if u in ["me", "self"]
            else u.lower().strip("@") if isinstance(u, str)
            else u for u in users
        )

    async def __call__(self, mtclient: "motogram.MotoClient", chat: Chat):
        return (chat.from_user
                and (chat.from_user.id in self
                     or (chat.from_user.username
                         and chat.from_user.username.lower() in self)
                     or ("me" in self
                         and chat.from_user.is_self)))

class group(Qualifier, set):
    def __init__(self, groups: Union[int, str, List[Union[int, str]]] = None):
        groups = [] if groups is None else groups if isinstance(groups, list) else [groups]

        super().__init__(
            "me" if c in ["me", "self"]
            else c.lower().strip("@") if isinstance(c, str)
            else c for c in groups
        )

    async def __call__(self, mtclient: "motogram.MotoClient", chat: Chat):
        return (chat.group
                and (chat.group.id in self
                     or (chat.group.username
                         and chat.group.username.lower() in self)
                     or ("me" in self
                         and chat.from_user
                         and chat.from_user.is_self
                         and not chat.out)))
