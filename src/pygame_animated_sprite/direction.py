from __future__ import annotations

from typing import Iterable, Iterator


class DirectionIterable(Iterable):
    def __init__(self, repeat: float, frame_length: int) -> None:
        self.repeat: float = repeat
        self.frame_length: int = frame_length
        return

    def __iter__(self) -> Iterator:
        raise NotImplementedError


class DirectionIterator(Iterator):
    def __init__(self, repeat: float, frame_length: int) -> None:
        super().__init__()
        self.repeat: float = repeat
        self.frame_length: int = frame_length
        self.index: int = 0
        return

    def __next__(self) -> int:
        raise NotImplementedError


class Forward(DirectionIterable):
    def __iter__(self) -> ForwardIterator:
        return ForwardIterator(self.repeat, self.frame_length)


class ForwardIterator(DirectionIterator):
    def __init__(self, repeat, frame_length) -> None:
        super().__init__(repeat=repeat, frame_length=frame_length)
        return

    def __next__(self) -> int:
        if self.frame_length == 0:
            raise StopIteration

        frame_index: int = self.index
        if frame_index == self.frame_length - 1:
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
    def __init__(self, repeat, frame_length) -> None:
        super().__init__(repeat=repeat, frame_length=frame_length)
        self.index = frame_length - 1
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


class PingPong(DirectionIterable):
    def __init__(self, repeat, frame_length) -> None:
        super().__init__(repeat, frame_length)
        return

    def __iter__(self) -> PingPongIterator:
        return PingPongIterator(self.repeat, self.frame_length)


class PingPongIterator(DirectionIterator):
    def __init__(self, repeat, frame_length) -> None:
        super().__init__(repeat, frame_length)
        self._direction: int = 1
        return

    def __next__(self) -> int:
        if self.frame_length == 0:
            raise StopIteration

        frame_index: int = self.index
        if frame_index == -1 and self._direction == -1:
            self.repeat -= 1
            if self.repeat == 0:
                raise StopIteration

            self.index = 0
            return frame_index

        if frame_index == -1 and self._direction == -1:
            self._direction = 1
        if frame_index == self.frame_length - 1 and self._direction == 1:
            self._direction = -1

        self.index += self._direction
        return frame_index


class PingPongReverse(DirectionIterable):
    def __init__(self, repeat, frame_length) -> None:
        super().__init__(repeat, frame_length)
        return

    def __iter__(self) -> PingPongReverseIterator:
        return PingPongReverseIterator(self.repeat, self.frame_length)


class PingPongReverseIterator(DirectionIterator):
    def __init__(self, repeat, frame_length) -> None:
        super().__init__(repeat, frame_length)
        self.index = frame_length - 1
        self._direction: int = -1
        return

    def __next__(self) -> int:
        if self.frame_length == 0:
            raise StopIteration

        frame_index: int = self.index
        if frame_index == self.frame_length and self._direction == 1:
            self.repeat -= 1
            if self.repeat == 0:
                raise StopIteration

            self.index = self.frame_length - 1
            return frame_index

        if frame_index == 0 and self._direction == -1:
            self._direction = 1
        if frame_index == self.frame_length and self._direction == 1:
            self._direction = -1

        self.index += self._direction
        return frame_index
