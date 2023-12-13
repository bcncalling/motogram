from typing import Callable
from motogram import MotoClient
from motogram.qualifiers import Qualifiers
from motogram.types import BackQuery
from motogram.handlers.handler import Handler

class BackQueryHandler:
    """The CallbackQuery handler class. Used to handle callback queries coming from inline buttons.
    It is intended to be used with :meth:`~pyrogram.MotoClient.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~motogram.MotoClient.on_back_query` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new CallbackQuery arrives. It takes *(mtclient, back_query)*
            as positional arguments (look at the section below for a detailed description).

        qualifiers (:obj:`Qualifiers`):
            Pass one or more qualifiers to allow only a subset of callback queries to be passed
            in your callback function.

    Other parameters:
        mtclient (:obj:`~motogram.MotoClient`):
            The Client itself, useful when you want to call other API methods inside the message handler.

        back_query (:obj:`~motogram.types.BackQuery`):
            The received callback query.
    """

    def __init__(self, callback: Callable, qualifiers=None):
        self.callback = callback
        self.qualifiers = qualifiers or Qualifiers.create()
        self.mtclient = None

    async def check_update(self, mtclient: MotoClient, back_query: BackQuery):
        """Internal method to check whether the given update should be handled by the handler."""
        self.mtclient = mtclient
        return await self.qualifiers(mtclient, back_query)

    async def handle_update(self, _, back_query: BackQuery):
        """Internal method to handle the given update."""
        await self.callback(self.mtclient, back_query)
