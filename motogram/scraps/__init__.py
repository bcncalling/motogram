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

from ..save_session import SaveSession
from ..go_start import Go, Start
from ..restart_stop import Restart, Stop
from ..stop_trans import StopTrans
from ..handlers import AddHandler, RemoveHandler

class scraps (
    SaveSession,
    Go,
    Start,
    Restart,
    Stop,
    StopTrans,
    AddHandler,
    RemoveHandler
):
    pass
  
