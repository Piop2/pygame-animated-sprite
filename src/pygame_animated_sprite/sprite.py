from __future__ import annotations

from typing import Optional, Sequence, final
from os import PathLike
from pathlib import Path

import pygame.image
from pygame import Surface, Vector2

from .timer import CountUpTimer
from .direction import (
    DirectionIterable,
    DirectionIterator,
    Forward,
)
from .struct import Tag, Frame
from .encoder.base import (
    AnimatedSpriteEncoder,
    AnimatedSpriteData,
    UnsupportedFileFormatError,
)


@final
class AnimatedSprite:
    def __init__(
        self,
        frames: Sequence[Frame],
        repeat: int = 0,
        direction: Optional[type[DirectionIterable]] = None,
        tags: Optional[dict[str, Tag]] = None,
    ) -> None:
        self.__frames: list[Frame] = list(frames)

        if tags is None:
            tags = dict()
        self.__tags: dict[str, Tag] = tags

        # origin repeat
        if repeat == 0:
            repeat = float("inf")
        self.__repeat: float = float(repeat)

        if direction is None:
            direction = Forward
        self.__direction: DirectionIterable = direction(
            repeat=repeat, frame_length=len(frames)
        )

        self.__timer: CountUpTimer = CountUpTimer()

        self.__direction_iterator: DirectionIterator = iter(self.__direction)
        self.__index: int = next(self.__direction_iterator)
        return

    def __len__(self) -> int:
        return len(self.__frames)

    def __getitem__(self, key: int | str | slice) -> Frame | AnimatedSprite:
        if isinstance(key, int):  # index
            return self.__frames[key]

        elif isinstance(key, str):  # slice by key
            return self.slice_by_tag(key)

        elif isinstance(key, slice):  # slice by slice obj
            return AnimatedSprite(self.__frames[key])

        raise TypeError
        return

    @classmethod
    def load(
        cls: type[AnimatedSprite],
        *paths: str | PathLike,
        encoder: Optional[AnimatedSpriteEncoder] = None,
    ) -> AnimatedSprite:
        if encoder is None:

            class DefaultEncoder(AnimatedSpriteEncoder):
                def load_file(self, path: Path) -> AnimatedSpriteData:
                    if path.suffix not in [".png", ".jpeg", ".jpg"]:
                        raise UnsupportedFileFormatError
                    return AnimatedSpriteData(frames=[pygame.image.load(path)])

            encoder = DefaultEncoder()

        data: AnimatedSpriteData = encoder.load(*paths)

        return cls(
            data.frames,
            data.repeat,
            data.direction,
            data.tags,
        )

    @classmethod
    def from_images(
        cls: type[AnimatedSprite],
        images: Sequence[Surface],
        durations: Sequence[int],
        repeat: int = 0,
        direction: Optional[type[DirectionIterable]] = None,
    ) -> AnimatedSprite:
        if len(frames) != len(durations):
            raise ValueError

        frames: list[Frame] = []
        for image, duration in zip(images, durations):
            frames.append(Frame(image, duration))

        return cls(frames, repeat, direction)

    @property
    def frames(self) -> tuple[Frame]:
        return tuple(self.__frames)

    @frames.setter
    def frames(self, new: Sequence[Frame]) -> None:
        self.__frames = list(new)
        self.reset()
        return

    @property
    def tags(self) -> dict[str, Tag]:
        return self.__tags

    @tags.setter
    def tags(self, new: dict[str, Tag]) -> None:
        self.__tags = new
        return

    @property
    def repeat(self) -> int:
        return self.__repeat

    @repeat.setter
    def repeat(self, new: int) -> None:
        self.__direction.repeat = new
        self.reset()
        return

    @property
    def index(self) -> int:
        return self.__index

    @property
    def direction(self) -> type[DirectionIterable]:
        return self.__direction.__class__

    @direction.setter
    def direction(self, new: type[DirectionIterable]) -> None:
        self.__direction = new(repeat=self.__repeat, frame_length=len(self.__frames))
        self.reset()
        return

    def get_time(self) -> int:
        return self.__timer.get_time()

    def get_current_frame(self) -> Frame:
        if not self.__frames:
            raise RuntimeError

        return self.__frames[self.__index]

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

    def slice_by_tag(self, tag_name: str) -> AnimatedSprite:
        if tag_name not in self.__tags:
            raise KeyError

        main_tag: Tag = self.__tags[tag_name]

        sub_tags: list[Tag] = []
        for tag in list(self.__tags.values()):
            if tag == main_tag:
                continue

            if main_tag.start <= tag.start and tag.end <= main_tag.end:
                new_start = tag.start - main_tag.start
                new_end = main_tag.end - tag.end

                sub_tags.append(
                    Tag(tag.name, new_start, new_end, tag.direction, tag.repeat)
                )

        return AnimatedSprite(
            self.__frames[main_tag.start : main_tag.end + 1],
            main_tag.repeat,
            main_tag.direction,
            sub_tags,
        )

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

    def draw(self, surface: Surface, dest: tuple[int, int] | Vector2) -> None:
        surface.blit(self.render(), dest)
        return
