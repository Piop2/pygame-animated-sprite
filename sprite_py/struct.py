from __future__ import annotations

from dataclasses import dataclass

from pygame import Surface

from pygame_animated_sprite.direction import DirectionIterable


@dataclass(frozen=True)
class Tag:
    name: str
    start: int
    end: int
    direction: type[DirectionIterable]
    repeat: int


@dataclass(frozen=True)
class Frame:
    image: Surface
    duration: int
