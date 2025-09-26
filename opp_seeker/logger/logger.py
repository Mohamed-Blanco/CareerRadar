from opp_seeker.logger.colors import Colors
from  opp_seeker.general_params import MODE

import threading
import logging
import inspect
import sys


class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self, level=str.upper(MODE)):
        self.logger = logging.getLogger("Logger")
        self.logger.setLevel(level)
        self.logger.propagate = False

        if not self.logger.handlers:
            formatter = self._get_colored_formatter()

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def _get_colored_formatter(self):
        class ColoredFormatter(logging.Formatter):
            def format(self, record):
                frame = inspect.stack()[8]  # Adjust index to reach the caller
                module = inspect.getmodule(frame[0])
                module_name = module.__name__ if module else ''
                class_name = ''
                if 'self' in frame[0].f_locals:
                    class_name = frame[0].f_locals['self'].__class__.__name__
                function_name = frame[3]
                caller_name = f"{class_name}.{function_name}".strip('.')

                color = Colors.WHITE  # default to white
                if record.levelno == logging.DEBUG:
                    color = Colors.CYAN
                elif record.levelno == logging.INFO:
                    color = Colors.GREEN
                elif record.levelno == logging.WARNING:
                    color = Colors.YELLOW
                elif record.levelno == logging.ERROR:
                    color = Colors.RED
                elif record.levelno == logging.CRITICAL:
                    color = Colors.PURPLE

                record.msg = f"{color}{record.msg}{Colors.RESET}"
                record.name = caller_name
                return super().format(record)

        return ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def set_level(self, level):
        self.logger.setLevel(level)

    def get_logger(self):
        return self.logger




class ExampleClass:
    def example_method(self):
        logger = Logger().get_logger()
        logger.debug("This is a debug message from ExampleClass.example_method")
        logger.info("This is an info message from ExampleClass.example_method")
        logger.warning("This is a warning message from ExampleClass.example_method")
        logger.error("This is an error message from ExampleClass.example_method")
        logger.critical("This is a critical message from ExampleClass.example_method")

class ExampleClass1:
    def __init__(self):
        self.logger = Logger().get_logger()
    def example_method(self):
        self.logger.debug("This is a debug message from ExampleClass1.example_method")


def main():
    example = ExampleClass()
    example.example_method()

    print("---------------------------------------------")
    sys.stdout.flush()


    example1 = ExampleClass1()
    example1.example_method()



    example.example_method()

    print("---------------------------------------------")
    sys.stdout.flush()


    example1.example_method()


if __name__ == "__main__" :
    main()








# class Logger:
#     _instance = None
#     _lock = threading.Lock()
#
#     def __init__(self):
#
#         self.logger = None
#         self.handler = None
#
#     def _initialize(self, level=logging.DEBUG):
#         self.logger = logging.getLogger("Logger")
#         self.logger.setLevel(level)
#         self.logger.propagate = False
#
#         if not self.logger.handlers:
#             console_handler = logging.StreamHandler()
#             self.logger.addHandler(console_handler)
#     def __new__(cls, *args, **kwargs):
#         if not cls._instance:
#             with cls._lock:
#                 if not cls._instance:
#                     cls._instance = super().__new__(cls)
#                     cls._instance._initialize(*args, **kwargs)
#         return cls._instance
#
#
#     def get_logger(log_file='flask_app.log'):
#         """
#         Sets up a logger that writes to a specified file and also logs to the console.
#
#         :param log_file: The name of the log file.
#         :return: Configured logger object.
#         """
#         # Create a logger
#         logger = logging.getLogger(__name__)
#         logger.setLevel(logging.DEBUG)  # Set to the lowest level to capture all messages
#
#           # Ensure the handler captures all messages
#
#         # Create a console handler
#         console_handler = logging.StreamHandler()
#         console_handler.setLevel(logging.DEBUG)  # Ensure the handler captures all messages
#
#         # Create a formatter and set it for both handlers
#         formatter = logging.Formatter('[ %(asctime)s ] - "%(levelname)s" : %(message)s')
#         file_handler.setFormatter(formatter)
#         console_handler.setFormatter(formatter)
#
#         # Add both handlers to the logger
#         logger.addHandler(file_handler)
#         logger.addHandler(console_handler)
#
#         return logger
#
# # Example usage
