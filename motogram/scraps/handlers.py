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

from motogram import MotoClient
from motogram.handlers import DisconnectHandler
from motogram.handlers.handler import Handler

class AddHandler(MotoClient):
    def __init__(self, name):
        super().__init__(name)
        self.disconnect_handler = None  # Initialize disconnect_handler as None

    def add_handler(self, handler: Handler, group: int = 0):
        """Register an update handler.

        You can register multiple handlers, but at most one handler within a group will be used for a single update.

        Parameters:
            handler (``Handler``):
                The handler to be registered.

            group (``int``, *optional*):
                The group identifier, defaults to 0.

        Returns:
            ``tuple``: A tuple consisting of *(handler, group)*.

        Example:
            .. code-block:: python

                from motogram import MotoClient
                from motogram.handlers import ChatHandler

                async def hello(client, message):
                    print(message)

                app = MyClient("my_account")

                app.add_handler(ChatHandler(hello))

                app.go()
        """
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = handler.callback
        else:
            self.dispatcher.add_handler(handler, group)

        return handler, group

    def remove_handler(self, handler: Handler):
        """Remove an update handler.

        Parameters:
            handler (``Handler``):
                The handler to be removed.

        Returns:
            ``bool``: True if the handler was successfully removed, False otherwise.
        """
        if isinstance(handler, DisconnectHandler):
            return False  # DisconnectHandler cannot be removed
        else:
            return self.dispatcher.remove_handler(handler)
