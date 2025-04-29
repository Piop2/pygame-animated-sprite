from __future__ import annotations

from typing import Optional, Protocol, final
from os import PathLike
from pathlib import Path
from dataclasses import dataclass

from .direction import DirectionIterable
from .struct import Frame, Tag


class __Singleton(type):
    __instances: dict[str, __Singleton] = {}

    def __call__(cls: __Singleton, *args, **kwargs) -> any:
        if (class_name := cls.__class__.__name__) not in cls.__instances :
            cls.__instances[class_name] = super().__call__(*args, **kwargs)
        
        return cls.__instances[class_name]

@final
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
    
    @property
    def protocol(self) -> AnimatedSpriteLoaderProtocol:
        return self.__protocol

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
