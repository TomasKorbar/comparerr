"""Module containing ComparerrMessage class"""
class ComparerrMessage:
    """ComparerrMessage holds original message from pylint and its code context
    """
    def __init__(self, original_message, context):
        self.original_message = original_message
        self.context = context

    def display_message(self):
        """Print important information about error"""
        print("Message: %s" % self.original_message.msg)
        print("File: %s" % self.original_message.path)
        print("Line: %s" % self.original_message.line)
        print("Context: \n%s" % self.context)
