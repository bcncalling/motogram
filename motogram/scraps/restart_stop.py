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
import motogram

class Restart:
    async def restart(
        self: "MotoClient",
        block: bool = True
    ) -> "MotoClient":
        """Restart the MotoClient.

        This method will first call :meth:`~motogram.MotoClient.stop` and then :meth:`~motogram.MotoClient.start` in a row
        in order to restart a client using a single method.

        Parameters:
            block (``bool``, *optional*):
                Blocks the code execution until the client has been restarted. It is useful with ``block=False`` in case
                you want to restart the own client within an handler in order not to cause a deadlock.
                Defaults to True.

        Returns:
            :obj:`~motogram.MotoClient`: The restarted client itself.

        Raises:
            ConnectionError: In case you try to restart a stopped MotoClient.

        Example:
            .. code-block:: python

                from motogram import MotoClient

                app = MotoClient("my_account")

                async def main():
                    await app.start()
                    ...  # Invoke API methods
                    await app.restart()
                    ...  # Invoke other API methods
                    await app.stop()

                app.go(main())
        """

        async def do_it():
            await self.stop()
            await self.start()

        if block:
            await do_it()
        else:
            self.loop.create_task(do_it())

        return self

#stop
class Stop:
    async def stop(
        self: "MotoClient",
        block: bool = True
    ) -> "MotoClient":
        """Stop the MotoClient.

        This method disconnects the client from Telegram and stops the underlying tasks.

        Parameters:
            block (``bool``, *optional*):
                Blocks the code execution until the client has been stopped. It is useful with ``block=False`` in case
                you want to stop the own client *within* a handler in order not to cause a deadlock.
                Defaults to True.

        Returns:
            :obj:`~motogram.MotoClient`: The stopped client itself.

        Raises:
            ConnectionError: In case you try to stop an already stopped client.

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

        async def do_it():
            await self.terminate()
            await self.disconnect()

        if block:
            await do_it()
        else:
            self.loop.create_task(do_it())

        return self
