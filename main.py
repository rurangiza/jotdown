import unittest
from unittest import mock, mock
from io import StringIO

from sys import stdout



def greeting():
    print('Hi there!')


class TestPrompt(unittest.TestCase):

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_print(self, mock_stdout):
        greeting()
        self.assertEqual(mock_stdout.getvalue(), 'Hi there!\n')


if __name__ == '__main__':
    unittest.main()

