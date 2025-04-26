from typing import Protocol, Any
from pathlib import Path
from os import PathLike
import json

import pygame
from pygame import Surface

from pygame_animation.struct import Tag, Frame


class BaseLoader(Protocol):
    def __init__(self) -> None:
        pass

    def load_animation(self, path: str | Path | PathLike):
        pass


class AsepriteLoader(BaseLoader):
    def __init__(self) -> None:
        # TODO Aseprite export 옵션에 따라 그에 맞게 로드할 수 있게 옵션 추가

        super().__init__()
        pass

    def load_animation(self, path):
        pass
