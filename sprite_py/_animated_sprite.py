from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Sequence, Optional

from sprite_py._sprite import Sprite
from sprite_py.direction import Direction, Forward
from sprite_py.struct import Tag, Frame
from sprite_py._timer import CountUpTimer


class AnimatedSprite(ABC):
    def __init__(
        self,
        frames: Sequence[Frame],
        repeats: Optional[int] = None,
        direction: Optional[type[Direction]] = None,
        tags: Optional[list[Tag]] = None,
    ) -> None:
        if tags is None:
            tags = []
        if direction is None:
            direction = Forward

        self._frames: list[Frame] = list(frames)
        self.__repeats: Optional[int] = repeats
        self.__tags: dict[str, Tag] = {tag.name: tag for tag in tags}

        self.__is_playing: bool = False
        self.__timer: CountUpTimer = CountUpTimer()
        self.__direction: Direction = iter(
            direction(frame_count=len(frames), repeats=repeats)
        )
        self.__index: int = next(self.__direction)
        return

    def __len__(self) -> int:
        return len(self._frames)

    def __getitem__(self, item: int | str | slice) -> Sprite | AnimatedSprite:
        pass

    def __setitem__(self, key: int, value: Frame) -> None:
        self.insert_frame(index=key, frame=value)
        return

    @property
    def frames(self) -> list[Frame]:
        return self._frames

    @property
    def tags(self) -> dict[str, Tag]:
        return self.__tags

    @property
    def repeats(self) -> int:
        return self.__repeats

    @repeats.setter
    def repeats(self, new: Optional[int]) -> None:
        self.__repeats = new
        self.__direction = self.__direction.__class__(
            frame_count=len(self._frames), repeats=new
        )
        self.reset()
        return

    @property
    def current_index(self) -> int:
        return self.__index

    @property
    def direction(self) -> Direction:
        return self.__direction

    def insert_frame(self, index: int, frame: Frame) -> None:
        pass

    def slice_by_tag(self, tag_name: str) -> AnimatedSprite:
        pass

    def slice(self, start: int, end: int) -> AnimatedSprite:
        pass

    def is_playing(self) -> bool:
        return not self.__is_playing

    def play(self) -> None:
        self.__is_playing = True
        return

    def pause(self) -> None:
        self.__is_playing = False
        return

    def reset(self) -> None:
        self.__direction = iter(self.direction)
        self.__index = next(self.__direction)
        self.__timer.reset()
        self.play()
        return

    def update(self, time_delta: int) -> None:
        pass

    @abstractmethod
    def draw(self, target: Any):
        pass
