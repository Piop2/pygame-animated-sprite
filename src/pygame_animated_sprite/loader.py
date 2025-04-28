from __future__ import annotations

from typing import Optional, Protocol
from os import PathLike
from pathlib import Path
from dataclasses import dataclass

from .direction import DirectionIterable
from .struct import Frame, Tag


class __Singleton(type):
    __instance: Optional[__Singleton] = None

    def __call__(cls, *args, **kwargs) -> any:
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class AnimatedSpritLoader(metaclass=__Singleton):
    def __init__(
        self,
        path: str | PathLike,
        protocol: Optional[AnimatedSpriteLoaderProtocol] = None,
    ) -> None:
        super().__init__()

        self.__path: str | PathLike = path

        if protocol is None:

            class DefaultProtocol(AnimatedSpriteLoaderProtocol):
                pass

            protocol = DefaultProtocol()
        self.__protocol: AnimatedSpriteLoaderProtocol = protocol
        return

    @property
    def path(self) -> Path:
        return self.__path

    def load(self) -> LoadedAnimatedSprite:
        return self.__protocol.load(self.__path)


class AnimatedSpriteLoaderProtocol(Protocol):
    def load(self, path: str | PathLike) -> LoadedAnimatedSprite: ...


@dataclass(frozen=True)
class LoadedAnimatedSprite:
    frames: tuple[Frame, ...]
    repeat: int
    direction: DirectionIterable
    tags: dict[str, Tag]
