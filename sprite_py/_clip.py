from __future__ import annotations

from typing import Protocol

from sprite_py._texture import TextureProtocol


class ImageClipper(Protocol):
    def clip(self, x: int, y: int, width: int, height: int) -> TextureProtocol: ...
