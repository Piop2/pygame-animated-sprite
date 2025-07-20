import unittest

from pygame import Surface

from pygame_animated_sprite.direction import Forward
from pygame_animated_sprite.structures import Tag, Frame


class StructuresTestCase(unittest.TestCase):
    def setUp(self):
        self.frame = Frame(surface=Surface((0, 0)), duration=0)
        self.tag = Tag(name="", start=0, end=1, direction=Forward, repeat=1)
        return

    def test_frame_copy(self):
        copied_frame = self.frame.copy()

        self.assertIsNot(self.frame, copied_frame)
        self.assertIsNot(self.frame.surface, copied_frame.surface)
        self.assertEqual(self.frame.duration, copied_frame.duration)
        return

    def test_tag_copy(self):
        copied_tag = self.tag.copy()

        self.assertEqual(self.tag.name, copied_tag.name)
        self.assertEqual(self.tag.start, copied_tag.start)
        self.assertEqual(self.tag.end, copied_tag.end)
        self.assertEqual(self.tag.direction, copied_tag.direction)
        self.assertEqual(self.tag.repeat, copied_tag.repeat)
        return


if __name__ == "__main__":
    unittest.main()
