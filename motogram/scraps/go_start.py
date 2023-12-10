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
import inspect
from motogram import raw
import motogram
from motogram.scraps.idle import idle
import logging

log = logging.getLogger(__name__)

class Go:
    def go(
        self: "motogram.MotoClient",
        coroutine=None
    ):
        """Start the client, idle the main script and finally stop the client.

        When calling this method without any argument it acts as a convenience method that calls
        :meth:`~motogram.MotoClient.start`, :meth:`~motogram.idle` and :meth:`~motogram.MotoClient.stop` in sequence.
        It makes running a single client less verbose.

        In case a coroutine is passed as argument, runs the coroutine until it's completed and doesn't do any client
        operation. This is almost the same as :py:obj:`asyncio.run` except for the fact that Motogram's ``go`` uses the
        current event loop instead of a new one.

        If you want to run multiple clients at once, see :meth:`motogram.compose`.

        Parameters:
            coroutine (``Coroutine``, *optional*):
                Pass a coroutine to run it until it completes.

        Raises:
            ConnectionError: In case you try to run an already started client.

        Example:
            .. code-block:: python

                from motogram import MotoClient

                app = MotoClient("my_account")
                ...  # Set handlers up
                app.go()

            .. code-block:: python

                from motogram import MotoClient

                app = MotoClient("my_account")

                async def main():
                    async with app:
                        print(await app.get_me())

                app.go(main())
        """
        loop = asyncio.get_event_loop()
        go = loop.run_until_complete

        if coroutine is not None:
            go(coroutine)
        else:
            if inspect.iscoroutinefunction(self.start):
                go(self.start())
                go(idle())
                go(self.stop())
            else:
                self.start()
                go(idle())
                self.stop()


#start
class Start:
    async def start(
        self: "MotoClient"
    ) -> "MotoClient":
        """Start the client.

        This method connects the client to Telegram and, in case of new sessions, automatically manages the
        authorization process using an interactive prompt.

        Returns:
            :obj:`~motogram.MotoClient`: The started client itself.

        Raises:
            ConnectionError: In case you try to start an already started client.

        Example:
            .. code-block:: python

                from motogram import MotoClient

                app = MotoClient("my_account")

                async def main():
                    await app.start()
                    ...  # Invoke API methods
                    await app.stop()

                app.go(main())
        """
        is_authorized = await self.connect()

        try:
            if not is_authorized:
                await self.authorize()

            if not await self.storage.is_bot() and self.takeout:
                self.takeout_id = (await self.invoke(raw.functions.account.InitTakeoutSession())).id
                log.info("Takeout session %s initiated", self.takeout_id)

            await self.invoke(raw.functions.updates.GetState())
        except (Exception, KeyboardInterrupt):
            await self.disconnect()
            raise
        else:
            self.me = await self.get_me()
            await self.initialize()

            return self
