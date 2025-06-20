from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from pathlib import Path

from ..direction import DirectionIterable
from ..struct import Frame, Tag


@dataclass(frozen=True)
class AnimatedSpriteData:
    frames: Optional[tuple[Frame, ...]] = None
    repeat: Optional[int] = None
    direction: Optional[type[DirectionIterable]] = None
    tags: Optional[dict[str, Tag]] = None


# class __Singleton(type):
#     __instances: dict[str, __Singleton] = {}

#     def __call__(cls: __Singleton, *args, **kwargs) -> any:
#         if (class_name := cls.__class__.__name__) not in cls.__instances:
#             cls.__instances[class_name] = super().__call__(*args, **kwargs)

#         return cls.__instances[class_name]


class AnimatedSpriteEncoder:
    def load_file(self, path: Path) -> AnimatedSpriteData:
        raise NotImplementedError

    def load_folder(self, path: Path) -> AnimatedSpriteData:
        raise NotImplementedError

    def load(self, path: Path) -> AnimatedSpriteData:
        if path.is_file():
            return self.load_file(path)
        return self.load_folder(path)


class UnsupportedFileFormatError(Exception):
    pass
