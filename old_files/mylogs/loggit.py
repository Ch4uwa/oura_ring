"""
Author: Martin Karlsson
Email: mrtn.karlsson@gmail.com
"""
import logging
import os


class MyLogger:
    def __init__(self):
        filename = 'oura.log'
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.full_path = os.path.join(self.base_path, filename)
        self.formats = {
            'datetime1': '%d-%m-%Y %H:%M:%S %z',
            'datetime2': '%d-%b-%y %H:%M:%S',
            'info': '%(asctime)s %(name)s %(levelname)s %(message)s',
            'warning': '%(asctime)s %(name)s %(process)d %(levelname)s %(message)s'
        }

        # create logger
        logger = logging.getLogger(name)
        a = logging.Logger('a')
        
        # create handler
        file_handler = logging.FileHandler(self.full_path)
        console_handler = logging.StreamHandler()

        # set loglevel
        file_handler.setLevel(logging.WARNING)
        file_info_handler.setLevel(logging.INFO)
        console_handler.setLevel(logging.DEBUG)

        # create formatters
        file_formatter = logging.Formatter(
            fmt=self.formats['warning'],
            datefmt=self.formats["datetime1"])
        console_formatter = logging.Formatter(
            fmt=self.formats['warning'], datefmt=self.formats['datetime1'])

        # set formatter
        file_handler.setFormatter(file_formatter)
        file_info_handler.setFormatter(file_info_formatter)
        console_handler.setFormatter(console_formatter)

        # add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)        
