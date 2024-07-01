from unittest.mock import patch
from letschat.inout import stream, prompt
from io import StringIO
import pytest


class TestStream:


    def setup_method(self, method):
        self.long_text = """
        Once more the storm is howling, and half hi
        Under this cradle-hood and coverlid
        My child sleeps on. There is no obstacle
        But Gregory's wood and one bare hill
        Whereby the haystack- and roof-levelling wind,
        Bred on the Atlantic, can be stayed;
        And for an hour I have walked and prayed
        Because of the great gloom that is in my mind.
        """
    

    @patch('sys.stdout', new_callable=StringIO)
    def test_small_text(self, fake_out):
        stream("hello")
        assert fake_out.getvalue().strip() == "hello"


    @patch('sys.stdout', new_callable=StringIO)
    def test_long_text(self, fake_out):
        stream(self.long_text, delay=0)
        assert fake_out.getvalue().strip() == self.long_text.strip()


    @patch('sys.stdout', new_callable=StringIO)
    def test_empty(self, fake_out):
        stream("")
        assert fake_out.getvalue().strip() == ""


class TestPrompt:


    def setup_method(self, method):
        pass


    @patch('builtins.input', return_value='today was great')
    def test_valid_input(self, fake_in):
        answer = prompt('...')
        assert answer == 'today was great'
    

    @patch('builtins.input', return_value='')
    def test_empty_input_multiple_times(self, fake_in):
        with pytest.raises(EOFError):
            prompt('...')
    