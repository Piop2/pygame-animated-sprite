from __future__ import annotations

from dataclasses import dataclass

from pygame import Surface

from pygame_animated_sprite.direction import Direction


@dataclass
class Tag:
    name: str
    start: int
    end: int
    direction: type[Direction]
    repeat: int

    def copy(self) -> Tag:
        return Tag(
            name=self.name,
            start=self.start,
            end=self.end,
            direction=self.direction,
            repeat=self.repeat,
        )


@dataclass
class Frame:
    image: Surface
    duration: int

    def copy(self) -> Frame:
        return Frame(
            image=self.image,
            duration=self.duration,
        )
