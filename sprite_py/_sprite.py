from __future__ import annotations

from typing import Optional, Any
from abc import ABC, abstractmethod

from sprite_py._texture import TextureProtocol


class Sprite(ABC):
    def __init__(self, texture: TextureProtocol) -> None:
        self.__texture: TextureProtocol = texture

        self.__position_x: int = 0
        self.__position_y: int = 0

        self.__opacity: int = 0
        self.__rotation: int = 0

        self.__scale_x: float = 1.0
        self.__scale_y: float = 1.0
        return

    def get_position(self) -> tuple[int, int]:
        return self.__position_x, self.__position_y

    def set_position(self, x: Optional[float] = None, y: Optional[float] = None):
        if x is not None:
            self.__scale_x = x

        if x is not None:
            self.__scale_y = y
        return

    def get_texture(self) -> TextureProtocol:
        return self.__texture

    def get_size(self) -> tuple[int, int]:
        return self.__texture.get_size()

    def get_opacity(self) -> int:
        return self.__opacity

    def set_opacity(self, value: int) -> None:
        if not 0 <= value <= 255:
            raise ValueError

        self.__opacity = value
        return

    def get_rotation(self) -> int:
        return self.__rotation

    def set_rotation(self, degree: int) -> None:
        self.__rotation = degree
        self.__rotation %= 360
        return

    def rotate(self, degree: int) -> None:
        self.__rotation += degree
        self.__rotation %= 360
        return

    def get_scale(self) -> tuple[float, float]:
        return self.__scale_x, self.__scale_y

    def set_scale(self, x: Optional[float] = None, y: Optional[float] = None):
        if x is not None:
            if x <= 0:
                raise ValueError
            self.__scale_x = x

        if x is not None:
            if x <= 0:
                raise ValueError
            self.__scale_y = y
        return

    @abstractmethod
    def draw(self, target: Any) -> None: ...
