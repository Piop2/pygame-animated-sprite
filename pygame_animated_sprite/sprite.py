from __future__ import annotations

from typing import Optional, Sequence, final
from pathlib import Path

import pygame.image
from pygame import Surface, Vector2

from pygame_animated_sprite.timer import CountUpTimer
from pygame_animated_sprite.direction import (
    DirectionIterable,
    DirectionIterator,
    Forward,
)
from pygame_animated_sprite.struct import Tag, Frame
from pygame_animated_sprite.encoder.base import (
    AnimatedSpriteEncoder,
    AnimatedSpriteData,
    UnsupportedFileFormatError,
)


@final
class AnimatedSprite:
    def __init__(
        self,
        frames: Sequence[Frame],
        repeat: int,
        direction: type[DirectionIterable],
        tags: dict[str, Tag],
    ) -> None:
        self.__frames: list[Frame] = list(frames)
        self.__tags: dict[str, Tag] = tags

        # origin repeat
        self.__repeat: int
        if repeat <= 0:
            self.__repeat = repeat = 0

        self.__direction: DirectionIterable = direction(
            repeat=repeat,
            frame_length=len(frames),
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
            return AnimatedSprite(
                frames=self.__frames[key], repeat=0, direction=Forward, tags={}
            )

        raise TypeError
        return

    @classmethod
    def load(
        cls: type[AnimatedSprite],
        path: str,
        encoder: Optional[AnimatedSpriteEncoder] = None,
    ) -> AnimatedSprite:
        if encoder is None:

            class DefaultEncoder(AnimatedSpriteEncoder):
                def load_file(self, path: Path) -> AnimatedSpriteData:
                    if path.suffix not in [".png", ".jpeg", ".jpg"]:
                        raise UnsupportedFileFormatError
                    return AnimatedSpriteData(
                        frames=(Frame(image=pygame.image.load(path), duration=0),)
                    )

            encoder = DefaultEncoder()

        data: AnimatedSpriteData = encoder.load(Path(path))

        return cls(
            frames=data.frames if data.frames is not None else [],
            repeat=data.repeat if data.repeat is not None else 0,
            direction=data.direction if data.direction is not None else Forward,
            tags=data.tags if data.tags is not None else {},
        )

    @classmethod
    def from_surfaces(
        cls: type[AnimatedSprite],
        surfaces: Sequence[Surface],
        durations: Sequence[int],
        repeat: int = 0,
        direction: Optional[type[DirectionIterable]] = None,
    ) -> AnimatedSprite:
        if len(surfaces) != len(durations):
            raise ValueError

        frames: list[Frame] = []
        for image, duration in zip(surfaces, durations):
            frames.append(Frame(image, duration))

        if direction is None:
            direction = Forward

        return cls(frames=frames, repeat=repeat, direction=direction, tags={})

    @property
    def frames(self) -> tuple[Frame, ...]:
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
        self.__direction = new(
            repeat=self.__repeat,
            frame_length=len(self.__frames),
        )
        self.reset()
        return

    def get_time(self) -> int:
        return self.__timer.time

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

        sub_tags: dict[str, Tag] = {}
        for name, tag in self.__tags.items():
            if tag == main_tag:
                continue

            if main_tag.start <= tag.start and tag.end <= main_tag.end:
                new_start: int = tag.start - main_tag.start
                new_end: int = main_tag.end - tag.end

                sub_tags[name] = Tag(
                    name=tag.name,
                    start=new_start,
                    end=new_end,
                    direction=tag.direction,
                    repeat=tag.repeat,
                )

        return AnimatedSprite(
            frames=self.__frames[main_tag.start : main_tag.end + 1],
            repeat=main_tag.repeat,
            direction=main_tag.direction,
            tags=sub_tags,
        )

    def update(self, time_delta: int) -> None:
        if not self.is_playing():
            return

        if self.__timer.time >= self.__frames[self.__index].duration:
            try:
                self.__index = next(self.__direction_iterator)
            except StopIteration:
                self.pause()

            overflow_time: int = (
                self.__timer.time - self.__frames[self.__index].duration
            )
            self.__timer.reset()
            self.__timer.update(overflow_time)

        self.__timer.update(time_delta)
        return

    def render(self) -> Surface:
        return self.__frames[self.__index].image

    def draw(self, surface: Surface, dest: tuple[int, int] | Vector2) -> None:
        surface.blit(self.render(), dest)
        return
