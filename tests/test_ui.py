from unittest.mock import patch
from jotdown.ui import CLI, Editor
from io import StringIO
import pytest


""" CLI (Command-Line Interface) """

class TestStream:


    def setup_method(self, method):
        self.long_text = """\
        Once more the storm is howling, and half hi\
        Under this cradle-hood and coverlid\
        My child sleeps on. There is no obstacle\
        But Gregory's wood and one bare hill\
        Whereby the haystack- and roof-levelling wind,\
        Bred on the Atlantic, can be stayed;\
        And for an hour I have walked and prayed\
        Because of the great gloom that is in my mind.\
        """
    

    @patch('sys.stdout', new_callable=StringIO)
    def test_small_text(self, fake_out):
        ui = CLI()
        ui.stream("hello")
        assert fake_out.getvalue().strip() == "hello"


    @patch('sys.stdout', new_callable=StringIO)
    def test_long_text(self, fake_out):
        ui = CLI()
        ui.stream(self.long_text, delay=0)
        assert fake_out.getvalue().strip() == self.long_text.strip()


    @patch('sys.stdout', new_callable=StringIO)
    def test_empty(self, fake_out):
        ui = CLI()
        ui.stream("")
        assert fake_out.getvalue().strip() == ""


""" Editor """