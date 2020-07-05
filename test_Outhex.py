import unittest
from OutHex import OutHex


class TestOutHex(unittest.TestCase):

    def test_creator(self):
        oh = OutHex()
        testing_str = "323232323232323232323232323232ff"
        answer = [['00000000'],
                  [['32', '32', '32', '32', '32', '32', '32', '32', '32', '32', '32', '32', '32', '32', '32', 'ff']],
                  ['222222222222222ÿ']]
        self.assertEqual(oh.creator(testing_str), answer)


if __name__ == '__main__':
    unittest.main()
