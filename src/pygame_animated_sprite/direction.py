from __future__ import annotations

from typing import Iterable, Iterator


class DirectionIterable(Iterable):
    def __init__(self, repeat: int, frame_length: int) -> None:
        self.repeat: int = repeat
        self.frame_length: int = frame_length
        return

    def __iter__(self) -> Iterator:
        raise NotImplementedError


class DirectionIterator(Iterator):
    def __init__(self, repeat: int, frame_length: int, start_index: int = 0) -> None:
        super().__init__()
        self.repeat: int = repeat
        self.frame_length: int = frame_length
        self.index: int = start_index
        return

    def __next__(self) -> int:
        raise NotImplementedError


class Forward(DirectionIterable):
    def __iter__(self) -> ForwardIterator:
        return ForwardIterator(self.repeat, self.frame_length)


class ForwardIterator(DirectionIterator):
    def __init__(self, repeat, frame_length, start_index=0) -> None:
        super().__init__(repeat=repeat, frame_length=frame_length, start_index=0)
        return

    def __next__(self) -> int:
        if self.frame_length == 0:
            raise StopIteration

        frame_index: int = self.index
        if frame_index == self.frame_length:
            self.repeat -= 1
            if self.repeat == 0:
                raise StopIteration

            self.index = 0
            return frame_index

        self.index += 1
        return frame_index


class Reverse(DirectionIterable):
    def __iter__(self) -> ReverseIterator:
        return ReverseIterator(self.repeat, self.frame_length)


class ReverseIterator(DirectionIterator):
    def __init__(self, repeat, frame_length, start_index=0) -> None:
        super().__init__(
            repeat=repeat, frame_length=frame_length, start_index=frame_length - 1
        )
        return

    def __next__(self) -> int:
        if self.frame_length == 0:
            raise StopIteration

        frame_index: int = self.index
        if frame_index == 0:
            self.repeat -= 1
            if self.repeat == 0:
                raise StopIteration

            self.index = self.frame_length - 1
            return frame_index

        self.index -= 1
        return frame_index
