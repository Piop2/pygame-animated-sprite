from __future__ import annotations

from typing import Iterable, Iterator


class DirectionIterable(Iterable):
    def __init__(self, repeat: int, frame_length: int) -> None:
        self.__repeat: int = repeat
        self.__frame_length: int = frame_length
        return

    def __iter__(self) -> Iterator:
        raise NotImplementedError

    def get_repeat(self) -> int:
        return self.__repeat

    def get_frame_length(self) -> int:
        return self.__frame_length


class DirectionIterator(Iterator):
    def __init__(self, repeat: int, frame_length: int) -> None:
        super().__init__()
        self._repeat: int = repeat
        self._frame_length: int = frame_length
        self._index: int
        return

    def __next__(self) -> int:
        raise NotImplementedError


class Forward(DirectionIterable):
    def __iter__(self) -> ForwardIterator:
        return ForwardIterator(self.get_repeat(), self.get_frame_length())


class ForwardIterator(DirectionIterator):
    def __init__(self, repeat, frame_length) -> None:
        super().__init__(repeat, frame_length)
        self._index = 0
        return

    def __next__(self) -> int:
        if self._frame_length == 0:
            raise StopIteration

        frame_index: int = self._index
        if frame_index == self._frame_length:
            self._repeat -= 1
            if self._repeat == 0:
                raise StopIteration

            self._index = 0
            return frame_index

        self._index += 1
        return frame_index


class Reverse(DirectionIterable):
    def __iter__(self) -> ReverseIterator:
        return ReverseIterator(self.get_repeat(), self.get_frame_length())


class ReverseIterator(DirectionIterator):
    def __init__(self, repeat, frame_length) -> None:
        super().__init__(repeat, frame_length)
        self._index = frame_length - 1
        return

    def __next__(self) -> int:
        if self._frame_length == 0:
            raise StopIteration

        frame_index: int = self._index
        if frame_index == 0:
            self._repeat -= 1
            if self._repeat == 0:
                raise StopIteration

            self._index = self._frame_length - 1
            return frame_index

        self._index -= 1
        return frame_index
