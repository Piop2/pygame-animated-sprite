from __future__ import annotations

from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

from pygame_animated_sprite.direction import Direction
from pygame_animated_sprite.structures import Frame, Tag


@dataclass(frozen=True)
class SpriteSheetData:
    frames: Optional[tuple[Frame, ...]] = field(default=None)
    repeat: int = field(default=-1)
    direction: Optional[type[Direction]] = field(default=None)
    tags: Optional[dict[str, Tag]] = field(default=None)


class BaseSpriteSheetLoader:
    def load_file(self, path: Path) -> SpriteSheetData:
        raise NotImplementedError("file load is not implemented.")

    def load_folder(self, path: Path) -> SpriteSheetData:
        raise NotImplementedError("folder load is not implemented.")

    def load(self, path: Path) -> SpriteSheetData:
        if path.is_file():
            return self.load_file(path)
        return self.load_folder(path)


class UnsupportedFileFormatError(Exception):
    pass
