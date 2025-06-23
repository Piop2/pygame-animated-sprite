from __future__ import annotations

from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from pygame_animated_sprite.direction import DirectionIterable
from pygame_animated_sprite.struct import Frame, Tag


@dataclass(frozen=True)
class AnimatedSpriteData:
    frames: Optional[tuple[Frame, ...]] = None
    repeat: Optional[int] = None
    direction: Optional[type[DirectionIterable]] = None
    tags: Optional[dict[str, Tag]] = None


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
