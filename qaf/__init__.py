__version__ = "1.2.1"

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

from qaf.automation.core.qaf_exceptions import KeyNotFoundError

from qaf.automation.core.configurations_manager import ConfigurationsManager as CM
from qaf.automation.keys.application_properties import ApplicationProperties as AP
from qaf.automation.core.resources_manager import ResourcesManager


ResourcesManager().set_up()

if not CM().contains_key(key=AP.TESTING_APPROACH):
    raise KeyNotFoundError(message=AP.TESTING_APPROACH + ' e.g. behave, pytest')

if CM().get_str_for_key(key=AP.TESTING_APPROACH).lower() == 'behave':
    from behave.runner_util import load_step_modules
    import os

    import qaf.automation.step_def as step_def_path
    step_def_path = str(os.path.abspath(step_def_path.__file__)).replace('/__init__.py', '')

    SUBSTEP_DIRS = [step_def_path]
    load_step_modules(SUBSTEP_DIRS)
