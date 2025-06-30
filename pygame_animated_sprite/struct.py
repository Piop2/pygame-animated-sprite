from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, asdict

from pygame import Surface

from pygame_animated_sprite.direction import DirectionIterable


@dataclass(frozen=True)
class Tag:
    name: str
    start: int
    end: int
    direction: type[DirectionIterable]
    repeat: int

    def copy(self) -> Tag:
        return self.__class__(**deepcopy(asdict(self)))


@dataclass(frozen=True)
class Frame:
    image: Surface
    duration: int

    def copy(self) -> Frame:
        return self.__class__(**deepcopy(asdict(self)))
