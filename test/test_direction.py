import unittest

from pygame_animated_sprite.direction import Forward, Reverse, PingPong, PingPongReverse


class DirectionTestCase(unittest.TestCase):
    def setUp(self):
        self.forward = iter(Forward(5, 1))
        self.reverse = iter(Reverse(5, 1))
        self.pingpong = iter(PingPong(3, 1))
        self.pingpong_reverse = iter(PingPongReverse(3, 1))
        return

    def test_forward(self):
        self.assertEqual(next(self.forward), 0)
        self.assertEqual(next(self.forward), 1)
        self.assertEqual(next(self.forward), 2)
        self.assertEqual(next(self.forward), 3)
        self.assertEqual(next(self.forward), 4)

        with self.assertRaises(StopIteration):
            next(self.forward)

        return

    def test_reverse(self):
        self.assertEqual(next(self.reverse), 4)
        self.assertEqual(next(self.reverse), 3)
        self.assertEqual(next(self.reverse), 2)
        self.assertEqual(next(self.reverse), 1)
        self.assertEqual(next(self.reverse), 0)

        with self.assertRaises(StopIteration):
            next(self.reverse)

        return

    def test_pingpong(self):
        self.assertEqual(next(self.pingpong), 0)
        self.assertEqual(next(self.pingpong), 1)
        self.assertEqual(next(self.pingpong), 2)
        self.assertEqual(next(self.pingpong), 1)
        self.assertEqual(next(self.pingpong), 0)

        with self.assertRaises(StopIteration):
            next(self.pingpong)

        return

    def test_pingpong_reverse(self):
        self.assertEqual(next(self.pingpong_reverse), 2)
        self.assertEqual(next(self.pingpong_reverse), 1)
        self.assertEqual(next(self.pingpong_reverse), 0)
        self.assertEqual(next(self.pingpong_reverse), 1)
        self.assertEqual(next(self.pingpong_reverse), 2)

        with self.assertRaises(StopIteration):
            next(self.pingpong_reverse)

        return


if __name__ == "__main__":
    unittest.main()
