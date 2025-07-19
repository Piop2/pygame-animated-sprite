from __future__ import annotations

from dataclasses import dataclass, replace

from pygame import Surface

from pygame_animated_sprite.direction import Direction


@dataclass(frozen=True)
class Tag:
    name: str
    start: int
    end: int
    direction: type[Direction]
    repeat: int

    def copy(self) -> Tag:
        return replace(self)


@dataclass(frozen=True)
class Frame:
    image: Surface
    duration: int

    def copy(self) -> Frame:
        return replace(self)
