from __future__ import annotations

from typing import Optional, Sequence, final
from pathlib import Path

import pygame.image
from pygame import Surface, Vector2

from pygame_animated_sprite._timer import CountUpTimer
from pygame_animated_sprite.direction import (
    Direction,
    Forward,
)
from pygame_animated_sprite.structures import Tag, Frame
from pygame_animated_sprite.loader.base import (
    BaseSpriteSheetLoader,
    SpriteSheetData,
    UnsupportedFileFormatError,
)


def load(
    path: str,
    loader: Optional[BaseSpriteSheetLoader] = None,
) -> AnimatedSprite:
    return AnimatedSprite.load(path, loader)


@final
class AnimatedSprite:
    """
    A class for handling animated sprites in Pygame.
    """

    def __init__(
        self,
        frames: Sequence[Frame],
        repeats: int,
        direction: type[Direction],
        tags: dict[str, Tag],
    ) -> None:
        """
        Initializes the AnimatedSprite.

        :param frames: A sequence of Frame objects.
        :param repeats: The number of times to repeat the animation.
        :param direction: The direction of the animation (e.g., Forward, Reverse).
        :param tags: A dictionary of tags for slicing the animation.
        """
        self.__frames: list[Frame] = list(frames)
        self.__tags: dict[str, Tag] = tags

        self.__direction: Direction = direction(
            frame_count=len(frames),
            repeats=repeats,
        )

        self.__timer: CountUpTimer = CountUpTimer()

        iter(self.__direction)
        self.__index: int = next(self.__direction)
        return

    def __len__(self) -> int:
        """Returns the number of frames in the animation."""
        return len(self.__frames)

    def __getitem__(self, key: int | str | slice) -> Frame | AnimatedSprite:
        """
        Gets a frame or a new AnimatedSprite by index, tag, or slice.
        """
        if isinstance(key, int):  # index
            return self.__frames[key]

        elif isinstance(key, str):  # slice by key
            return self.slice_by_tag(key)

        elif isinstance(key, slice):  # slice by slice obj
            return AnimatedSprite(
                frames=self.__frames[key], repeats=0, direction=Forward, tags={}
            )

        raise TypeError

    @classmethod
    def load(
        cls: type[AnimatedSprite],
        path: str,
        loader: Optional[BaseSpriteSheetLoader] = None,
    ) -> AnimatedSprite:
        """
        Loads an animated sprite from a file.

        :param path: The path to the file.
        :param loader: The encoder to use for loading the file.
        :return: An AnimatedSprite object.
        """
        if loader is None:

            class DefaultEncoder(BaseSpriteSheetLoader):
                def load_file(self, _path: Path) -> SpriteSheetData:
                    if _path.suffix not in [".png", ".jpeg", ".jpg"]:
                        raise UnsupportedFileFormatError
                    return SpriteSheetData(
                        frames=(Frame(surface=pygame.image.load(_path), duration=0),)
                    )

            loader = DefaultEncoder()

        data: SpriteSheetData = loader.load(Path(path))

        return cls(
            frames=data.frames if data.frames is not None else [],
            repeats=data.repeat if data.repeat is not None else -1,
            direction=data.direction if data.direction is not None else Forward,
            tags=data.tags if data.tags is not None else {},
        )

    @classmethod
    def from_surfaces(
        cls: type[AnimatedSprite],
        surfaces: Sequence[Surface],
        durations: Sequence[int],
        repeats: int = -1,
        direction: Optional[type[Direction]] = None,
    ) -> AnimatedSprite:
        """
        Creates an AnimatedSprite from a sequence of surfaces and durations.
        """
        if len(surfaces) != len(durations):
            raise ValueError

        frames: list[Frame] = []
        for image, duration in zip(surfaces, durations):
            frames.append(Frame(image, duration))

        if direction is None:
            direction = Forward

        return cls(frames=frames, repeats=repeats, direction=direction, tags={})

    @property
    def frames(self) -> tuple[Frame, ...]:
        """The frames of the animation."""
        return tuple(self.__frames)

    @frames.setter
    def frames(self, new: Sequence[Frame]) -> None:
        self.__frames = list(new)
        self.reset()
        return

    @property
    def tags(self) -> dict[str, Tag]:
        """The tags for slicing the animation."""
        return self.__tags

    @tags.setter
    def tags(self, new: dict[str, Tag]) -> None:
        self.__tags = new
        return

    @property
    def repeat(self) -> int:
        """The number of times to repeat the animation."""
        return self.__direction.repeats

    @repeat.setter
    def repeat(self, new: int) -> None:
        self.__direction.repeats = new
        self.reset()
        return

    @property
    def index(self) -> int:
        """The current frame index."""
        return self.__index

    @property
    def direction(self) -> type[Direction]:
        """The direction of the animation."""
        return self.__direction.__class__

    @direction.setter
    def direction(self, new: type[Direction]) -> None:
        self.__direction = new(
            frame_count=len(self.__frames),
            repeats=self.repeat,
        )
        self.reset()
        return

    def get_time(self) -> int:
        """Gets the current time of the animation timer."""
        return self.__timer.time

    def get_current_frame(self) -> Frame:
        """Gets the current frame of the animation."""
        if not self.__frames:
            raise RuntimeError

        return self.__frames[self.__index]

    def is_playing(self) -> bool:
        """Returns True if the animation is playing."""
        return not self.__timer.is_paused()

    def play(self) -> None:
        """Plays the animation."""
        self.__timer.unpause()
        return

    def pause(self) -> None:
        """Pauses the animation."""
        self.__timer.pause()
        return

    def reset(self) -> None:
        """Resets the animation to the beginning."""
        self.play()
        self.__timer.reset()
        iter(self.__direction)
        self.__index = next(self.__direction)
        return

    def slice_by_tag(self, tag_name: str) -> AnimatedSprite:
        """
        Creates a new AnimatedSprite from a slice of the original.
        """
        if tag_name not in self.__tags:
            raise KeyError

        tag: Tag = self.__tags[tag_name]

        return AnimatedSprite(
            frames=self.__frames[tag.start : tag.end + 1],
            repeats=tag.repeat,
            direction=tag.direction,
            tags={},
        )

    def update(self, time_delta: int) -> None:
        """
        Updates the animation by a given time delta.
        """
        if not self.is_playing():
            return

        if self.__timer.time >= self.__frames[self.__index].duration:
            try:
                self.__index = next(self.__direction)
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
        """Renders the current frame of the animation."""
        return self.__frames[self.__index].surface

    def draw(self, surface: Surface, dest: tuple[int, int] | Vector2) -> None:
        """Draws the current frame of the animation to a surface."""
        surface.blit(self.render(), dest)
        return
