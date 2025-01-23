from __future__ import annotations

from abc import ABC, abstractmethod


class BaseTimer(ABC):
    def __init__(self, time: int) -> None:
        super().__init__()
        self._time: int = time
        self._is_paused: bool = False
        return

    def get_time(self) -> int:
        return self._time

    def is_paused(self) -> bool:
        return self._is_paused

    def unpause(self) -> None:
        self._is_paused = False
        return

    def pause(self) -> None:
        self._is_paused = True
        return

    @abstractmethod
    def reset(self) -> None: ...

    @abstractmethod
    def update(self, ms: int) -> None: ...


class CountUpTimer(BaseTimer):
    def __init__(self) -> None:
        super().__init__(time=0)

    def reset(self) -> None:
        pass

    def update(self, ms: int) -> None:
        pass


class CountDownTimer(BaseTimer):
    def __init__(self, time) -> None:
        super().__init__(time)
        self._total_time: int = time
        return

    def get_total_time(self) -> int:
        return self._total_time

    def is_done(self) -> bool:
        return self._time == 0

    def reset(self) -> None:
        pass

    def update(self, ms: int) -> None:
        pass
