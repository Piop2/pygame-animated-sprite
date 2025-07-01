from __future__ import annotations

from typing import Protocol


class TextureProtocol(Protocol):
    def bind(self) -> None: ...

    def unbind(self) -> None: ...

    def get_size(self) -> tuple[int, int]: ...
