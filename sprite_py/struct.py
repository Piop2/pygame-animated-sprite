from __future__ import annotations

from dataclasses import dataclass

from sprite_py._sprite import Sprite


@dataclass(frozen=True)
class Tag:
    name: str
    start: int
    end: int
    # direction: type[DirectionIterable]
    repeat: int


@dataclass(frozen=True)
class Frame:
    sprite: Sprite
    duration: int
