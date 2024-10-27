'''
@author: No.47
@file: CustomException.py
@time: 2024/8/10 19:00
@desc: 自定义异常
'''

class CustomException(Exception):
    def __init__(self, message, type):
        self.message = message
        self.type = type

    def __str__(self):
        return f"Custom Exception: {self.message} (Type: {self.type})"


#获取数据结果为空异常
class ListLengthZeroError(CustomException):
    def __init__(self, message="可下载数据为空！"):
        self.message = message
        super().__init__(self.message,"List is None")

class DataValidationError(CustomException):
    def __init__(self, message):
        super().__init__(message, "Data Validation")

class FileNotFoundError(CustomException):
    def __init__(self, message):
        super().__init__(message, "File Not Found")