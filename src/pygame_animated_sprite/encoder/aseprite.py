from __future__ import annotations

from pathlib import Path

from .base import AnimatedSpriteEncoder, AnimatedSpriteData


# TODO Aseprite EXPORT FILE 인코더입니다

class AsepriteEncoder(AnimatedSpriteEncoder):
    """Aseprite exported file encoder"""
    def __init__(self) -> None:
        return

    def load_file(self, path: Path) -> AnimatedSpriteData:
        pass

    def load_folder(self, path: Path) -> AnimatedSpriteData:
        pass
