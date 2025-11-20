from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Literal, TypedDict

import pygame.image
from pygame import Surface

from pygame_animated_sprite._utils import clip_surface
from pygame_animated_sprite.structures import Frame, Tag
from pygame_animated_sprite.direction import (
    Direction,
    Forward,
    Reverse,
    PingPong,
    PingPongReverse,
)
from pygame_animated_sprite.loader.base import (
    BaseSpriteSheetLoader,
    SpriteSheetData,
)

__JsonFormat = Literal["array", "hash"]
__Size = TypedDict("__Size", {"w": int, "h": int})
__Rect = TypedDict("__Rect", {"x": int, "y": int, "w": int, "h": int})
__Frames = TypedDict(
    "__Frames",
    {
        "frame": __Rect,
        "rotated": bool,
        "trimmed": bool,
        "spriteSourceSize": __Rect,
        "sourceSize": __Size,
        "duration": int,
    },
)
__Tag = TypedDict(
    "__Tag",
    {
        "name": str,
        "from": int,
        "to": int,
        "repeat": int,
        "direction": Literal["forward", "reverse", "pingpong", "pingpong_reverse"],
        "color": str,
    },
)
__Meta = TypedDict(
    "__Meta",
    {
        "app": str,
        "version": str,
        "image": str,
        "format": str,
        "size": __Size,
        "scale": str,
        "frameTags": list[__Tag],
    },
)


class AsepriteSpriteSheetEncoder(BaseSpriteSheetLoader):
    """Aseprite sprite sheet encoder"""

    # minimum supported version
    MIN_SUPPORTED_VERSION = (1, 2)

    def __init__(
        self,
        json_format: __JsonFormat,
    ) -> None:
        self.json_format: __JsonFormat = json_format

        # meta
        # self.layers
        # self.slices
        return

    def __warn_if_unsupported_version(self, version: str) -> None:
        _ver = tuple(map(int, version.split(".")[0:2]))
        print(_ver)
        if _ver >= self.MIN_SUPPORTED_VERSION:
            return

        warnings.warn(
            f"version {version} is not supported and may cause errors.", UserWarning
        )
        return

    def __load_tags(self, frame_tags: list[__Tag]) -> dict[str, Tag]:
        tags: dict[str, Tag] = {}
        for tag_data in frame_tags:
            direction: type[Direction] = Forward
            match tag_data["direction"]:
                case "forward":
                    direction = Forward
                case "reverse":
                    direction = Reverse
                case "pingpong":
                    direction = PingPong
                case "pingpong_reverse":
                    direction = PingPongReverse
                case _:
                    warnings.warn(
                        f"{tag_data['direction']} direction is not supported. Using 'Forward' as default.",
                        UserWarning,
                    )

            tag_repeat: int
            try:
                tag_repeat = int(tag_data["repeat"])
            except KeyError:
                tag_repeat = -1

            if tag_repeat == 0:
                tag_repeat = -1

            tags[tag_data["name"]] = Tag(
                name=tag_data["name"],
                start=tag_data["from"],
                end=tag_data["to"] + 1,
                direction=direction,
                repeat=tag_repeat,
            )

        return tags

    def __load_frames(
        self, image: Surface, frames_raw: dict[str, __Frames] | list[__Frames]
    ) -> tuple[Frame, ...]:
        frames_list: list[__Frames]
        if self.json_format == "hash":
            frames_list = list(frames_raw.values())
        else:  # self.json_format == "array"
            frames_list = frames_raw

        frames: list[Frame] = []
        for frame_data in frames_list:
            rect: __Rect = frame_data["frame"]
            duration = frame_data["duration"]

            frames.append(
                Frame(
                    clip_surface(
                        surface=image,
                        dest=(rect["x"], rect["y"]),
                        size=(rect["w"], rect["h"]),
                    ),
                    duration,
                )
            )
        return tuple(frames)

    def load_file(self, path: Path) -> SpriteSheetData:
        with open(path.as_posix(), "r") as file:
            data = json.load(file)

        meta: __Meta = data["meta"]
        self.__warn_if_unsupported_version(meta["version"])

        image = pygame.image.load(str(path.parent / meta["image"]))
        tags = self.__load_tags(meta["frameTags"])
        frames = self.__load_frames(image, data["frames"])

        # repeat=-1 (infinite), direction=Forward (default)
        return SpriteSheetData(
            frames=frames, repeat=-1, direction=Forward, tags=tags
        )
