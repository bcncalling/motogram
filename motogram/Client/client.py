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

import asyncio
import functools
import inspect
import logging
import os
import platform
import re
import shutil
import sys
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timedelta
from hashlib import sha256
from importlib import import_module
from io import StringIO, BytesIO
from mimetypes import MimeTypes
from pathlib import Path
from typing import Union, List, Optional, Callable, AsyncGenerator
from motogram.strings import Session
from motogram.store import MemoryStorage, FileStorage
from .dispatcher import Dispatcher
from motogram.types import User, TermsOfService
import logging
import time
import motogram
from motogram.methods import Methods

log = logging.getLogger(__name__)

class MsgId:
    last_time = 0
    offset = 0
    def __new__(cls) -> int:
        now = int(time.time())
        cls.offset = (cls.offset + 4) if now == cls.last_time else 0
        msg_id = (now * 2 ** 32) + cls.offset
        cls.last_time = now

        return msg_id
      

class MotoClient(Methods):
    """
    MotoClient is a Telegram MTProto library for building Telegram bots.

    Parameters:
        name (``str``):
            A name for the client, e.g.: "bot".

        api_id (``int`` | ``str``, *optional*):
            The *api_id* part of the Telegram API key, as integer or string.
            E.g.: 12345 or "12345".

        api_hash (``str``, *optional*):
            The *api_hash* part of the Telegram API key, as string.
            E.g.: "0123456789abcdef0123456789abcdef".

        bot_token (``str``, *optional*):
            Pass the Bot API token to create a bot session, e.g.: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
            Only applicable for new sessions.

        session_string (``str``, *optional*):
            Pass a session string to load the session in-memory.
            Implies ``in_memory=True``.

        in_memory (``bool``, *optional*):
            Pass True to start an in-memory session that will be discarded as soon as the client stops.
            In order to reconnect again using an in-memory session without having to log in again, you can use
            :meth:`~mototgram.Client.client.export_session_string` before stopping the client to get a session string you can
            pass to the ``session_string`` parameter.
            Defaults to False.

        phone_number (``str``, *optional*):
            Pass the phone number as a string (with the Country Code prefix included) to avoid entering it manually.
            Only applicable for new sessions.

        phone_code (``str``, *optional*):
            Pass the phone code as a string (for test numbers only) to avoid entering it manually.
            Only applicable for new sessions.

        password (``str``, *optional*):
            Pass the Two-Step Verification password as a string (if required) to avoid entering it manually.
            Only applicable for new sessions.

        custom_plugins (``dict``, *optional*):
            Custom Plugins settings as dict, e.g.: *dict(root="custom_plugins")*.
    """

    def __init__(self, name: str, api_id: Union[int, str] = None, api_hash: str = None, bot_token: str = None,
                 session_string: str = None, in_memory: bool = False, phone_number: str = None, phone_code: str = None,
                 password: str = None, custom_plugins: dict = None):

        super().__init__()

        self.name = name
        self.api_id = int(api_id) if api_id else None
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.session_string = session_string
        self.in_memory = in_memory
        self.phone_number = phone_number
        self.phone_code = phone_code
        self.password = password
        self.plugins = custom_plugins
        if self.session_string:
            self.storage = MemoryStorage(self.name, self.session_string)
        elif self.in_memory:
            self.storage = MemoryStorage(self.name)
        else:
            self.storage = FileStorage(self.name)         
        self.dispatcher = Dispatcher(self)
        self.rnd_id = MsgId
        self.session = None
        self.media_sessions = {}
        self.media_sessions_lock = asyncio.Lock()
        self.save_file_semaphore = asyncio.Semaphore(self.max_concurrent_transmissions)
        self.get_file_semaphore = asyncio.Semaphore(self.max_concurrent_transmissions)
        self.is_connected = None
        self.is_initialized = None
        self.takeout_id = None
        self.disconnect_handler = None
        self.me: Optional[User] = None
        self.message_cache = Cache(10000)
