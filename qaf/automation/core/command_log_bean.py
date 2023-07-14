#  Copyright (c) 2022 Infostretch Corporation
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#  #
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
from dataclasses import dataclass


@dataclass
class CommandLogBean:
    """
    @author: Chirag Jayswal
    """

    def __init__(self) -> None:
        self.commandName = ''
        self.args = []
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

    @subLogs.setter
    def subLogs(self, value: list):
        self.__subLogs = value

    def add_subLogs(self, sub_log: "CommandLogBean") -> None:
        self.__subLogs.append(sub_log)

    @property
    def duration(self) -> int:
        return self.__duration

    @duration.setter
    def duration(self, value: int) -> None:
        self.__duration = value

    def to_json_dict(self) -> dict:
        # args_array = []
        # if self.args:
        #     for key, value in self.args.items():
        #         args_array.append(str(key) + ':' + str(value))

        _dict = {
            "commandName": self.commandName,
            "args": list(map(str, self.args)),
            "result": self.result,
            "subLogs": self.subLogs,
            "duration": self.duration,
        }
        return _dict

    def to_string(self) -> str:
        string = f'Command: {self.commandName} {self.args} {self.result}'
        # for key, value in self.args.items():
        #     string = string + ' ' + str(key) + ':' + str(value)
        # string = string + str(self.result)
        return string
