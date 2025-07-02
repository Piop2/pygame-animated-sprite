from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator, Optional, Self


class Direction(ABC, Iterator[int]):
    """
    Abstract base class for an animation direction iterator.
    Defines the core structure for iterating over frame indices.
    """

    def __init__(self, frame_count: int, repeats: Optional[int] = 1) -> None:
        """
        Initializes the Direction iterator.

        :param frame_count: The total number of frames in the animation.
        :param repeats: The number of times to repeat the animation. Use None for infinite repeats.
        """
        if frame_count < 0:
            raise ValueError("frame_count cannot be negative.")
        if repeats is not None and repeats < 0:
            raise ValueError("repeats cannot be negative.")
        self.frame_count = frame_count
        self._initial_repeats = repeats
        self._repeats_left = self._initial_repeats
        self._current_index = 0

    def __iter__(self) -> Self:
        """Resets the state for iteration and returns the iterator itself."""
        self._repeats_left = self._initial_repeats
        self._reset_for_iteration()
        return self

    @abstractmethod
    def __next__(self) -> int:
        """
        Returns the next frame index.
        Raises StopIteration when the animation is complete.
        """
        raise NotImplementedError

    def _reset_for_iteration(self) -> None:
        """Resets the internal state for a new iteration loop."""
        self._current_index = 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(frame_count={self.frame_count}, repeats={self._initial_repeats})"


class Forward(Direction):
    """Iterates through frames in the forward direction (e.g., 0, 1, 2, 0, 1, 2...)."""

    def _reset_for_iteration(self) -> None:
        self._current_index = 0

    def __next__(self) -> int:
        if self.frame_count == 0 or (
            self._repeats_left is not None and self._repeats_left <= 0
        ):
            raise StopIteration

        frame_index = self._current_index
        self._current_index += 1

        if self._current_index == self.frame_count:
            if self._repeats_left is not None:
                self._repeats_left -= 1
            if self._repeats_left is None or self._repeats_left > 0:
                self._current_index = 0

        return frame_index


class Reverse(Direction):
    """Iterates through frames in the reverse direction (e.g., 2, 1, 0, 2, 1, 0...)."""

    def _reset_for_iteration(self) -> None:
        self._current_index = self.frame_count - 1 if self.frame_count > 0 else 0

    def __next__(self) -> int:
        if self.frame_count == 0 or (
            self._repeats_left is not None and self._repeats_left <= 0
        ):
            raise StopIteration

        frame_index = self._current_index
        self._current_index -= 1

        if self._current_index < 0:
            if self._repeats_left is not None:
                self._repeats_left -= 1
            if self._repeats_left is None or self._repeats_left > 0:
                self._current_index = self.frame_count - 1

        return frame_index


class PingPong(Direction):
    """Iterates through frames forwards and then backwards (e.g., 0, 1, 2, 1, 0, 1, 2...)."""

    def __init__(self, frame_count: int, repeats: Optional[int] = 1) -> None:
        super().__init__(frame_count, repeats)
        self._direction = 1 if self.frame_count > 1 else 0

    def _reset_for_iteration(self) -> None:
        self._current_index = 0
        self._direction = 1 if self.frame_count > 1 else 0

    def __next__(self) -> int:
        if self.frame_count == 0 or (
            self._repeats_left is not None and self._repeats_left <= 0
        ):
            raise StopIteration

        # If there is only one frame, repeat frame 0.
        if self.frame_count == 1:
            if self._repeats_left is not None:
                self._repeats_left -= 1
            return 0

        frame_index = self._current_index

        # Moving backwards at the start point completes a cycle.
        if self._current_index == 0 and self._direction == -1:
            if self._repeats_left is not None:
                self._repeats_left -= 1
            if self._repeats_left is not None and self._repeats_left <= 0:
                return frame_index
            # Start a new cycle
            self._direction = 1
            self._current_index += self._direction
        # Change direction when moving forward at the end point.
        elif self._current_index == self.frame_count - 1 and self._direction == 1:
            self._direction = -1
            self._current_index += self._direction
        else:
            # Continue moving in the current direction.
            self._current_index += self._direction

        return frame_index
