import unittest

from pygame_animated_sprite.direction import (
    Forward,
    Reverse,
    PingPong,
    PingPongReverse,
)


class TestDirection(unittest.TestCase):
    def test_init(self):
        # Test case for repeats < -1
        d = Forward(frame_count=3, repeats=-5)
        self.assertEqual(d._initial_repeats, -1)

        # Test case for repeats = -1
        d = Forward(frame_count=3, repeats=-1)
        self.assertEqual(d._initial_repeats, -1)

        # Test case for repeats = 0
        d = Forward(frame_count=3, repeats=0)
        self.assertEqual(d._initial_repeats, 0)

        # Test case for repeats > 0
        d = Forward(frame_count=3, repeats=5)
        self.assertEqual(d._initial_repeats, 5)

        # Test ValueError for frame_count < 0
        with self.assertRaises(ValueError):
            Forward(frame_count=-1, repeats=1)

    def test_repr(self):
        d = Forward(frame_count=5, repeats=2)
        self.assertEqual(repr(d), "Forward(frame_count=5, repeats=2)")


class TestForward(unittest.TestCase):
    def test_iteration(self):
        # Test with repeats=1
        direction = Forward(frame_count=3, repeats=1)
        self.assertEqual(list(iter(direction)), [0, 1, 2])

        # Test with repeats=2
        direction = Forward(frame_count=2, repeats=2)
        self.assertEqual(list(iter(direction)), [0, 1, 0, 1])

        # Test with repeats=0
        direction = Forward(frame_count=3, repeats=0)
        self.assertEqual(list(iter(direction)), [])

        # Test with infinite repeats
        direction = Forward(frame_count=2, repeats=-1)
        iterator = iter(direction)
        self.assertEqual([next(iterator) for _ in range(5)], [0, 1, 0, 1, 0])

        # Test with frame_count=0
        direction = Forward(frame_count=0, repeats=5)
        self.assertEqual(list(iter(direction)), [])


class TestReverse(unittest.TestCase):
    def test_iteration(self):
        # Test with repeats=1
        direction = Reverse(frame_count=3, repeats=1)
        self.assertEqual(list(iter(direction)), [2, 1, 0])

        # Test with repeats=2
        direction = Reverse(frame_count=2, repeats=2)
        self.assertEqual(list(iter(direction)), [1, 0, 1, 0])

        # Test with repeats=0
        direction = Reverse(frame_count=3, repeats=0)
        self.assertEqual(list(iter(direction)), [])

        # Test with infinite repeats
        direction = Reverse(frame_count=2, repeats=-1)
        iterator = iter(direction)
        self.assertEqual([next(iterator) for _ in range(5)], [1, 0, 1, 0, 1])

        # Test with frame_count=0
        direction = Reverse(frame_count=0, repeats=5)
        self.assertEqual(list(iter(direction)), [])


class TestPingPong(unittest.TestCase):
    def test_iteration(self):
        # Test with repeats=1
        direction = PingPong(frame_count=4, repeats=1)
        self.assertEqual(list(iter(direction)), [0, 1, 2, 3, 2, 1])

        # Test with repeats=2
        direction = PingPong(frame_count=3, repeats=2)
        self.assertEqual(list(iter(direction)), [0, 1, 2, 1, 0, 1, 2, 1])

        # Test with repeats=0
        direction = PingPong(frame_count=3, repeats=0)
        self.assertEqual(list(iter(direction)), [])

        # Test with infinite repeats
        direction = PingPong(frame_count=3, repeats=-1)
        iterator = iter(direction)
        self.assertEqual(
            [next(iterator) for _ in range(10)], [0, 1, 2, 1, 0, 1, 2, 1, 0, 1]
        )

        # Test with frame_count=0
        direction = PingPong(frame_count=0, repeats=5)
        self.assertEqual(list(iter(direction)), [])

        # Test with frame_count=1
        direction = PingPong(frame_count=1, repeats=3)
        self.assertEqual(list(iter(direction)), [0, 0, 0])


class TestPingPongReverse(unittest.TestCase):
    def test_iteration(self):
        # Test with repeats=1
        direction = PingPongReverse(frame_count=4, repeats=1)
        self.assertEqual(list(iter(direction)), [3, 2, 1, 0, 1, 2])

        # Test with repeats=2
        direction = PingPongReverse(frame_count=3, repeats=2)
        self.assertEqual(list(iter(direction)), [2, 1, 0, 1, 2, 1, 0, 1])

        # Test with repeats=0
        direction = PingPongReverse(frame_count=3, repeats=0)
        self.assertEqual(list(iter(direction)), [])

        # Test with infinite repeats
        direction = PingPongReverse(frame_count=3, repeats=-1)
        iterator = iter(direction)
        self.assertEqual(
            [next(iterator) for _ in range(10)], [2, 1, 0, 1, 2, 1, 0, 1, 2, 1]
        )

        # Test with frame_count=0
        direction = PingPongReverse(frame_count=0, repeats=5)
        self.assertEqual(list(iter(direction)), [])

        # Test with frame_count=1
        direction = PingPongReverse(frame_count=1, repeats=3)
        self.assertEqual(list(iter(direction)), [0, 0, 0])


if __name__ == "__main__":
    unittest.main()
