import argparse


class ShowText(argparse.Action):

    def __init__(self, option_strings, text=None, dest=argparse.SUPPRESS, default=argparse.SUPPRESS, nargs=0):
        super().__init__(option_strings=option_strings, dest=dest, default=default, nargs=0)
        self._text = text

    def __call__(self, parser, namespace, values, option_string):
        print(self._text)
        quit()
