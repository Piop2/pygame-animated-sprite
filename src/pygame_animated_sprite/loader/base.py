from __future__ import annotations

from typing import Optional, final, Protocol
from os import PathLike
from pathlib import Path
from dataclasses import dataclass
from pathlib import Path

import pygame.image

from ..direction import DirectionIterable
from ..struct import Frame, Tag


@dataclass(frozen=True)
class AnimatedSpriteData:
    frames: Optional[tuple[Frame, ...]] = None
    repeat: Optional[int] = None
    direction: Optional[DirectionIterable] = None
    tags: Optional[dict[str, Tag]] = None


class __Singleton(type):
    __instances: dict[str, __Singleton] = {}

    def __call__(cls: __Singleton, *args, **kwargs) -> any:
        if (class_name := cls.__class__.__name__) not in cls.__instances:
            cls.__instances[class_name] = super().__call__(*args, **kwargs)

        return cls.__instances[class_name]


@final
class AnimatedSpriteLoader(metaclass=__Singleton):
    def __init__(
        self,
        *paths: str | PathLike,
        protocol: AnimatedSpriteLoadProtocol,
    ) -> None:
        super().__init__()

        self.__paths: list[Path] = [Path(path) for path in paths]
        self.__load_protocol: AnimatedSpriteLoadProtocol = protocol
        return

    @property
    def path(self) -> Path:
        return self.__path.as_posix()

    @property
    def protocol(self) -> AnimatedSpriteLoadProtocol:
        return self.__load_protocol

    def load(self) -> AnimatedSpriteData:
        frames: tuple[Frame] = ()
        repeat: int = 0
        direction: Optional[DirectionIterable] = None
        tags: dict[str, Tag] = {}

        for path in self.__paths:
            data: AnimatedSpriteData = self.__load_protocol.load(path)

            if data.frames is not None:
                frames += data.frames

            if data.repeat is not None:
                repeat = data.repeat

            if data.direction is not None:
                direction = data.direction

            if data.tags is not None:
                for tag_name, tag in data.tags.items():
                    tags[tag_name] = tag

        return AnimatedSpriteData(
            frames=frames, repeat=repeat, direction=direction, tags=tags
        )


class AnimatedSpriteLoadProtocol(Protocol):
    def load(self, path: Path) -> AnimatedSpriteData: ...


class UnsupportedFileFormatError(Exception):
    pass
