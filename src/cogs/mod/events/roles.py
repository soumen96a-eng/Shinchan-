from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from core import Shinchan

from core import Cog


class RoleEvents(Cog):
    def __init__(self, bot: Shinchan):
        self.bot = bot
