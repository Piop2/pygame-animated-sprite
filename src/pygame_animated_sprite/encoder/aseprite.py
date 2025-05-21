from __future__ import annotations

from typing import Literal, TypedDict
from pathlib import Path
import json

import pygame.image
from pygame import Surface

from ..direction import DirectionIterable, Forward, Reverse, PingPong, PingPongReverse
from ..struct import Frame, Tag
from .._utils import clip_surface
from .base import AnimatedSpriteEncoder, AnimatedSpriteData


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
    },
)
__Tag = TypedDict(
    "__Tag",
    {
        "name": str,
        "from": int,
        "to": int,
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


class AsepriteSpriteSheetEncoder(AnimatedSpriteEncoder):
    """Aseprite sprite sheet encoder"""

    def __init__(self, json_type: Literal["array", "hash"], tags: bool = False) -> None:
        self.json_type: Literal["array", "hash"] = json_type

        # meta
        self.tags: bool = tags
        # self.layers
        # self.slices
        return

    def load_file(self, path: Path) -> AnimatedSpriteData:
        if path.suffix != ".json":
            return

        frames: list[Frame] = []
        tags: list[Tag] = []

        data: dict[str, any] = json.load(path.as_posix)
        # ---------meta---------
        meta_data: __Meta = data["meta"]

        packed_image: Surface = pygame.image.load(f"{path.parent}/{meta_data['image']}")
        for tag_data in meta_data["frameTags"]:
            tag_direction: DirectionIterable
            match tag_data["direction"]:
                case "forward":
                    tag_direction = Forward
                case "reverse":
                    tag_direction = Reverse
                case "pingpong":
                    tag_direction = PingPong
                case "pingpong_reverse":
                    tag_direction = PingPongReverse
                case _:
                    NotImplementedError(
                        f"not implemented direction: {tag_data['direction']}"
                    )

            tag_repeat: int
            try:
                tag_repeat = int(tag_data["repeat"])
            except KeyError:
                tag_repeat = 0

            tags.append(
                Tag(
                    tag_data["name"],
                    tag_data["from"],
                    tag_data["to"] + 1,
                    tag_direction,
                    tag_repeat,
                )
            )

        # --------frames--------
        frame_list: list[dict[str, any]]
        if self.json_type == "hash":
            frame_list = list(data["frames"].values())

        frame_data: __Frames
        for frame_data in frame_list:
            frame_rect: __Rect = frame_data["frame"]
            duration: int = frame_data["duration"]
            frames.append(
                Frame(
                    clip_surface(
                        packed_image,
                        frame_rect["x"],
                        frame_rect["y"],
                        frame_rect["w"],
                        frame_rect["h"],
                    ),
                    duration,
                )
            )

        return AnimatedSpriteData(frames=frames, repeat=0, direction=Forward, tags=tags)

    def load_folder(self, path: Path) -> AnimatedSpriteData:
        pass
