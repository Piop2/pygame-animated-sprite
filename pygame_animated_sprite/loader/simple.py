from __future__ import annotations

from pathlib import Path

import pygame.image
from pygame import Surface

from pygame_animated_sprite.structures import Frame
from pygame_animated_sprite.direction import Forward
from pygame_animated_sprite._utils import clip_surface
from pygame_animated_sprite.loader import SpriteSheetData, UnsupportedFileFormatError
from pygame_animated_sprite.loader.base import BaseSpriteSheetLoader


class SimpleSpriteSheetLoader(BaseSpriteSheetLoader):
    """Simple sprite sheet loader"""

    def __init__(
        self,
        columns: int,
        rows: int,
        size: tuple[int, int],
        position: tuple[int, int] = (0, 0),
        padding: tuple[int, int] = (0, 0),
        default_duration: int = 100,
    ) -> None:
        if columns <= 0:
            raise ValueError("columns must be greater than 0.")
        self.columns = columns

        if rows <= 0:
            raise ValueError("rows must be greater than 0.")
        self.rows = rows

        self.width, self.height = size
        self.x, self.y = position
        self.padding_x, self.padding_y = padding

        self.default_duration = default_duration
        return

    def __load_frames(self, image: Surface) -> tuple[Frame, ...]:
        frames: list[Frame] = []

        for column in range(self.columns):
            for row in range(self.rows):
                # clip frame
                frames.append(
                    Frame(
                        surface=clip_surface(
                            image,
                            (
                                (self.width + self.padding_x) * row,
                                (self.height + self.padding_y) * column,
                            ),
                            (self.width, self.height),
                        ),
                        duration=self.default_duration,
                    )
                )

        return tuple(frames)

    def load_file(self, path: Path) -> SpriteSheetData:
        if path.suffix not in [".png", ".jpeg", ".jpg"]:
            raise UnsupportedFileFormatError

        image = pygame.image.load(path.as_posix())
        image = clip_surface(
            image,
            (self.x, self.y),
            (image.width - self.x, image.height - self.y),
        )

        frames = self.__load_frames(image)

        return SpriteSheetData(frames=frames, repeat=-1, direction=Forward)
