from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Optional

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


@dataclass
class Frame:
    image: Surface
    duration: int


class DirectionType(enum.Enum):
    FORWARD = enum.auto()
    REVERSE = enum.auto()
    PING_PONG = enum.auto()
    PING_PONG_REVERSE = enum.auto()


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
        self._frames: list[Frame] = frames

        if tags is None:
            tags = {}
        self._tags: dict[Tag] = tags

        self._timer: CountUpTimer = CountUpTimer()

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

        self._direction: DirectionIterable = direction_class(
            repeat=repeat, frame_length=len(frames)
        )
        self._direction_iterator: DirectionIterator = iter(self._direction)
        self._index: int = next(self._direction_iterator)
        return

    def get_frames(self) -> tuple[Frame]:
        return self._frames

    def get_index(self) -> int:
        return self._index

    def get_tags(self) -> tuple[Tag]:
        return tuple(self._tags.values())

    def is_playing(self) -> bool:
        return self._timer.is_paused()

    def play(self) -> None:
        self._timer.unpause()
        return

    def pause(self) -> None:
        self._timer.pause()
        return

    def reset(self) -> None: ...

    def split_by_tag(tag_name: str) -> Animation: ...

    def update(self, ms: int) -> None: ...

    def render(self) -> Surface: ...
