import inspect
from typing import Callable
import motogram
from motogram.Qualifiers import Qualifier

class Update:
    def stop_propagation(self):
        raise motogram.StopPropagation

    def continue_propagation(self):
        raise motogram.ContinuePropagation


class Handler:
    def __init__(self, callback: Callable, qualifiers: Qualifier = None):
        self.callback = callback
        self.qualifiers = qualifiers

    async def check(self, mtclient: "motogram.MotoClient", update: Update):
        if callable(self.qualifiers):
            if inspect.iscoroutinefunction(self.qualifiers.__call__):
                return await self.qualifiers(mtclient, update)
            else:
                return await mtclient.loop.run_in_executor(
                    mtclient.executor,
                    self.qualifiers,
                    mtclient, update
                )

        return True
