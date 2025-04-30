from __future__ import annotations

from typing import Optional, Protocol, final
from os import PathLike
from pathlib import Path
from dataclasses import dataclass
from pathlib import Path

from ..direction import DirectionIterable
from ..struct import Frame, Tag


class __Singleton(type):
    __instances: dict[str, __Singleton] = {}

    def __call__(cls: __Singleton, *args, **kwargs) -> any:
        if (class_name := cls.__class__.__name__) not in cls.__instances:
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

        self.__path: Path = Path(path)

        if protocol is None:

            class DefaultProtocol(AnimatedSpriteLoaderProtocol):
                def load(self, *paths: str | PathLike) -> AnimatedSpriteData:
                    # TODO 이거 쓰기
                    pass

            protocol = DefaultProtocol()
        self.__protocol: AnimatedSpriteLoaderProtocol = protocol
        return

    @property
    def path(self) -> Path:
        return self.__path.as_posix()

    @property
    def protocol(self) -> AnimatedSpriteLoaderProtocol:
        return self.__protocol

    def load(self) -> AnimatedSpriteData:
        return self.__protocol.load(self.__path)


class AnimatedSpriteLoaderProtocol(Protocol):
    def load(self, *paths: str | PathLike | Path) -> AnimatedSpriteData:
        paths: list[Path] = [Path(path) for path in paths if not isinstance(path, Path)]

        if len(paths) == 1:
            if paths[0].is_dir():
                return self.load_dir(paths[0])
            raise RuntimeError

        return self.load_files(*paths)

    def load_files(self, *paths: Path) -> AnimatedSpriteData:
        raise NotImplementedError

    def load_dir(self, path: Path) -> AnimatedSpriteData:
        raise NotImplementedError


@dataclass(frozen=True)
class AnimatedSpriteData:
    frames: tuple[Frame, ...]
    repeat: int
    direction: DirectionIterable
    tags: dict[str, Tag]
