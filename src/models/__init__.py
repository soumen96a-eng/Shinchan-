from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from core import Shinchan

from tortoise import models


class BaseDbModel(models.Model):
    """Base Model for all tortoise models"""

    class Meta:
        abstract = True

    bot: Shinchan


from .esports import *
from .helpers import *
from .misc import *
