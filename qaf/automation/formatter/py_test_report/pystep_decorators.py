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

from qaf.automation.formatter.py_test_report.meta_info import pytest_component
from qaf.automation.formatter.py_test_report.pytest_utils import PyTestStatus


class pystep(object):

    def __init__(self, keyword="[Func]", name=None):
        self.keyword = keyword
        self.name = name

    def before_step(self, step=None):
        pytest_component.PyTestStep._before_step(name=self.name, keyword=self.keyword, step=step)

    def after_step(self, status, exception=None):
        pytest_component.PyTestStep._after_step(status=status, exception=exception)

    def __call__(self, step):
        def wrapped_step(*args):
            self.before_step(step)
            step(*args)
            self.after_step(status=PyTestStatus.passed.name)

        return wrapped_step
