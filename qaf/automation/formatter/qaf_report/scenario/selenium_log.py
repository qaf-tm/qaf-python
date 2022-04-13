from collections import deque

from qaf.automation.core.singleton import Singleton


class SeleniumLog:
    def __init__(self) -> None:
        self.commandName = ''
        self.args = {}
        self.result = ''
        self.__subLogs = []
        self.duration = 0

    @property
    def commandName(self) -> str:
        return self.__commandName

    @commandName.setter
    def commandName(self, value: str) -> None:
        self.__commandName = value

    @property
    def args(self) -> dict:
        return self.__args

    @args.setter
    def args(self, value: dict) -> None:
        self.__args = value

    @property
    def result(self) -> str:
        return self.__result

    @result.setter
    def result(self, value: str) -> None:
        self.__result = value

    @property
    def subLogs(self) -> list:
        return self.__subLogs

    def add_subLogs(self, sub_log: str) -> None:
        self.__subLogs.append(sub_log)

    @property
    def duration(self) -> int:
        return self.__duration

    @duration.setter
    def duration(self, value: int) -> None:
        self.__duration = value

    def to_json_dict(self) -> dict:
        args_array = []
        for key, value in self.args.items():
            args_array.append(str(key) + ':' + str(value))

        _dict = {
            "commandName": self.commandName,
            "args": args_array,
            "result": self.result,
            "subLogs": self.subLogs,
            "duration": self.duration,
        }
        return _dict

    def to_string(self) -> str:
        string = 'Command: ' + self.commandName
        for key, value in self.args.items():
            string = string + ' ' + str(key) + ':' + str(value)
        string = string + str(self.result)
        return string


class SeleniumLogStack(metaclass=Singleton):
    def __init__(self) -> None:
        self.__selenium_log_stack = deque()

    def add_selenium_log(self, selenium_log: SeleniumLog) -> None:
        self.__selenium_log_stack.append(selenium_log.to_json_dict())

    def get_all_selenium_log(self) -> list:
        arr_selenium_log = []
        while self.__selenium_log_stack:
            selenium_log = self.__selenium_log_stack.popleft()
            arr_selenium_log.append(selenium_log)
        return arr_selenium_log