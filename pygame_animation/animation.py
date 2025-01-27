from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Optional

from pygame import Surface

from pygame_animation.timer import CountUpTimer


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
        repeat: int = -1,
        direction: Optional[DirectionType] = None,
        tags: Optional[dict[str, Tag]] = None
    ) -> None:
        if frames is None:
            frames = []
        self._frames: list[Frame] = frames

        self._total_repeat: int = repeat
        self._repeat: int = 0

        if direction is None:
            direction = DirectionType.FORWARD
        self._direction_type: DirectionType = direction

        if tags is None:
            tags = {}
        self._tags: dict[Tag] = tags

        self._timer: CountUpTimer = CountUpTimer()

        self._index: int
        self._direction: int
        match direction:
            case DirectionType.FORWARD | DirectionType.PING_PONG:
                self._index = 0
                self._direction = 1
            case DirectionType.REVERSE | DirectionType.PING_PONG_REVERSE:
                self._index = len(frames) - 1
                self._direction = -1
            case _:
                raise RuntimeError
        return
    
    def get_frames(self) -> tuple[Frame]:
        return self._frames
    
    def get_index(self) -> int:
        return self._index
    
    def get_total_repeat(self) -> int:
        return self._total_repeat
    
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
    
    def reset(self) -> None:
        ...

    def split_by_tag(tag_name: str) -> Animation:
        ...
    
    def update(self, ms: int) -> None:
        ...
    
    def render(self) -> Surface:
        ...
