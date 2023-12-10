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

class StopTrans:
    def stop_trans(self, reason: str = "Transmission stopped."):
        """Stop downloading or uploading a file.

        This method must be called inside a progress callback function in order to stop the transmission at the
        desired time. The progress callback is called every time a file chunk is uploaded/downloaded.

        Parameters:
            reason (``str``, *optional*):
                A message indicating the reason for stopping the transmission. Defaults to "Transmission stopped."

        Example:
            .. code-block:: python

                # Stop transmission once the upload progress reaches 50%
                async def progress(current, total, client):
                    if (current * 100 / total) > 50:
                        client.stop_transmission("Upload progress reached 50%.")

                async with app:
                    await app.send_doc(
                        "me", "file.zip",
                        progress=progress,
                        progress_args=(app,))
        """
        raise MotoClient.StopTrans(reason)
