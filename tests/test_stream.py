import unittest
from unittest import mock
from io import StringIO
from letschat.inout import stream


class TestStream(unittest.TestCase):

    @mock.patch('sys.stdout', StringIO)
    def test_basic_value(self, mock_stdout):
        stream('hello, world')
        self.assertEqual(mock_stdout.getvalue(), 'hello, world')
        # self.assertNotEqual(mock_stdout.getvalue(), 'hello, world%')


if __name__ == '__main__':
    unittest.main()