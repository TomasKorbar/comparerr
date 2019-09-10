"""Module containing ComparerrReporter class"""
from pylint.reporters import BaseReporter

class ComparerrReporter(BaseReporter):
    """Simple custom reporter for pylint which collects all messages about
    errors
    """
    # we will not be displaying messages with reporter so we do not need this
    # method
    _display = None

    def __init__(self):
        super().__init__()
        self.errors = []

    def handle_message(self, msg):
        self.errors.append(msg)
