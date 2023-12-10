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

import motogram
import struct

class SaveSession:
    async def save_session(self: "motogram.MotoClient"):
        """Save the current authorized session.

        Sessions are useful for storing in-memory authorized sessions for later reuse.

        Returns:
            ``bytes``: The session information saved as binary data.

        Example:
            .. code-block:: python

                session_data = await client.save_session()
        """
        session_info = await self.storage.save_session()
        return self.encode(session_info)

    def encode(self, session_info: dict) -> bytes:
        """Encode the session information into a binary format.

        Args:
            session_info (dict): The session information to encode.

        Returns:
            bytes: The binary representation of the session information.
        """
        encoded_data = struct.pack("I", len(session_info)) 
        for key, value in session_info.items():
            key_bytes = key.encode("utf-8")
            value_bytes = str(value).encode("utf-8")
            key_length = len(key_bytes)
            value_length = len(value_bytes)

            encoded_data += struct.pack("I", key_length)
            encoded_data += key_bytes
            encoded_data += struct.pack("I", value_length)
            encoded_data += value_bytes

        return encoded_data

    def decode(self, data: bytes) -> dict:
        """Decode the binary data into a session information dictionary.

        Args:
            data (bytes): The binary data to decode.

        Returns:
            dict: The decoded session information.
        """
        decoded_data = {}
        index = 0
        session_info_length = struct.unpack("I", data[index : index + 4])[0]
        index += 4

        for _ in range(session_info_length):
            key_length = struct.unpack("I", data[index : index + 4])[0]
            index += 4
            key = data[index : index + key_length].decode("utf-8")
            index += key_length

            value_length = struct.unpack("I", data[index : index + 4])[0]
            index += 4
            value = data[index : index + value_length].decode("utf-8")
            index += value_length

            decoded_data[key] = value

        return decoded_data
