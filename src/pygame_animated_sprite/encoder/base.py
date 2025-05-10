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
    direction: Optional[DirectionIterable] = None
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

    def load(self, *paths: str) -> AnimatedSpriteData:
        paths: list[Path] = [Path(str_path) for str_path in paths]

        frames: tuple[Frame] = ()
        repeat: int = 0
        direction: Optional[DirectionIterable] = None
        tags: dict[str, Tag] = {}

        for path in paths:
            data: AnimatedSpriteData
            if path.is_file():
                data = self.load_file(path)
            else:
                data = self.load_folder(path)

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


class UnsupportedFileFormatError(Exception):
    pass
