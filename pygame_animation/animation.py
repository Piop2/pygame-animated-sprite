from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Optional, final

from pygame import Surface

from pygame_animation.timer import CountUpTimer
from pygame_animation.direction import (
    DirectionIterable,
    DirectionIterator,
    Forward,
    Reverse,
)


@dataclass
class Tag:
    name: str
    start: int
    end: int
    direction: DirectionIterable


@dataclass
class Frame:
    image: Surface
    duration: int


class DirectionType(enum.Enum):
    FORWARD = enum.auto()
    REVERSE = enum.auto()
    PING_PONG = enum.auto()
    PING_PONG_REVERSE = enum.auto()


@final
class Animation:
    def __init__(
        self,
        frames: Optional[list[Frame]] = None,
        repeat: int = 0,
        direction_type: Optional[DirectionType] = None,
        tags: Optional[dict[str, Tag]] = None,
    ) -> None:
        if frames is None:
            frames = []
        self.__frames: list[Frame] = frames

        if tags is None:
            tags = {}
        self.__tags: dict[Tag] = tags

        self.__timer: CountUpTimer = CountUpTimer()

        if direction_type is None:
            direction_type = DirectionType.FORWARD
        direction_class: type[DirectionIterable]
        match direction_type:
            case DirectionType.FORWARD:
                direction_class = Forward
            case DirectionType.REVERSE:
                direction_class = Reverse
            case _:
                raise RuntimeError

        self.__direction: DirectionIterable = direction_class(
            repeat=repeat, frame_length=len(frames)
        )
        self.__direction_iterator: DirectionIterator = iter(self.__direction)
        self.__index: int = next(self.__direction_iterator)
        return

    def get_frames(self) -> tuple[Frame]:
        return self.__frames

    def get_index(self) -> int:
        return self.__index

    def get_tags(self) -> tuple[Tag]:
        return tuple(self.__tags.values())

    def is_playing(self) -> bool:
        return self.__timer.is_paused()

    def play(self) -> None:
        self.__timer.unpause()
        return

    def pause(self) -> None:
        self.__timer.pause()
        return

    def reset(self) -> None:
        self.play()
        self.__timer.reset()
        self.__direction_iterator = iter(self.__direction)
        self.__index = next(self.__direction_iterator)
        return

    def split_by_tag(tag_name: str) -> Animation: ...

    def update(self, ms: int) -> None:
        if not self.is_playing():
            return

        if self.__timer.get_time() >= self.__frames[self.__index].duration:
            try:
                self.__index = next(self.__direction_iterator)
            except StopIteration:
                self.pause()

        self.__timer.update(ms)
        return

    def render(self) -> Surface:
        return self.__frames[self.__index].image
