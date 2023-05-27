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

import re

import six
from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry as autoretry
from behave.model_core import Status

from qaf.automation.core.test_base import tear_down, start_step, end_step, get_command_logs, get_checkpoint_results, \
    is_verification_failed, clear_assertions_log
from qaf.automation.formatter.qaf_report.util.utils import step_status
from qaf.automation.integration.result_updator import update_result
from qaf.automation.integration.testcase_run_result import TestCaseRunResult
from qaf.automation.util.datetime_util import current_timestamp

OUTPUT_TEST_RESULTS_DIR = 'test-results'


class BaseEnvironment:
    def __init__(self):
        self.current_feature = None
        self.current_scenario = None
        self.current_step = None
        self.obj_scenario_meta_info = None

    def before_all(self, context):
        # ProjectEnvironment.set_up()

        # root_directory = os.path.join(OUTPUT_TEST_RESULTS_DIR, date_time())
        # create_directory(root_directory)
        # os.environ['REPORT_DIR'] = root_directory
        #before_all()
        pass

    def after_all(self, context):
        #ExecutionMetaInfo().endTime = current_timestamp()
        tear_down()

    def before_feature(self, context, feature):
        for scenario in feature.scenarios:
            if "autoretry" in scenario.effective_tags:
                autoretry(scenario, max_attempts=2)
        #
        # current_feature_directory = os.path.join(os.getenv('REPORT_DIR'), 'json', re.sub('[^A-Za-z0-9]+', ' - ',
        #                                                                                  re.sub('.feature', '',
        #                                                                                         feature.filename)))
        # create_directory(current_feature_directory)
        # os.environ['CURRENT_FEATURE_DIR'] = current_feature_directory

        #ExecutionMetaInfo().add_test(re.sub('[^A-Za-z0-9]+', ' - ', re.sub('.feature', '', feature.filename)))

        #FeatureOverView().startTime = current_timestamp()
        #FeatureOverView().add_class(feature.name)

    def after_feature(self, context, feature):
        #FeatureOverView().endTime = current_timestamp()
        pass

    def before_scenario(self, context, scenario):
        self.current_scenario = scenario
        # current_scenario_directory = os.path.join(os.getenv('CURRENT_FEATURE_DIR'), scenario.feature.name)
        # create_directory(current_scenario_directory)
        # os.environ['CURRENT_SCENARIO_DIR'] = current_scenario_directory

        #self.obj_scenario_meta_info = ScenarioMetaInfo()
        #self.obj_scenario_meta_info.startTime = current_timestamp()
        self.startTime = current_timestamp()
        clear_assertions_log()

    def after_scenario(self, context, scenario):

        status_name = scenario.status.name

        testcase_run_result = TestCaseRunResult()
        testcase_run_result.className = scenario.feature.name
        testcase_run_result.commandLogs = get_command_logs()
        testcase_run_result.starttime = self.startTime
        testcase_run_result.endtime = current_timestamp()#self.startTime + (scenario.duration * 1000)
        testcase_run_result.metaData = {
            "name": scenario.name,
            "resultFileName": scenario.name,
            "referece": six.text_type(scenario.location),
            "groups": scenario.effective_tags
        }
        testcase_run_result.executionInfo={
            "testName":"Py Test",
            "suiteName":"Py Suite",
            "driverCapabilities": {}
        }
        if scenario.description:
            testcase_run_result.metaData["description"] = scenario.description

        if scenario.status == Status.failed:
            steps = scenario.steps
            for step in steps:
                if step.status == Status.failed:
                    error_message = step.error_message
                    error_message = error_message.splitlines()
                    testcase_run_result.throwable = error_message

                    #Scenario(file_name=scenario.name).errorTrace = error_message
                elif step.status == Status.skipped or step.status == Status.untested:
                    # obj_step = Step()
                    # obj_step.start_behave_step(step)
                    # obj_step.stop_behave_step(step)
                    # Scenario(file_name=self.current_scenario.name).add_checkPoints(obj_step.obj_check_point)
                    # del obj_step
                    start_step(step.keyword + ' ' + step.name)
                    end_step(None)
        else:
            if is_verification_failed():
                status_name = 'failed'
            # checkPoints = Scenario(file_name=self.current_scenario.name).checkPoints
            # for checkPoint in checkPoints:
            #     if checkPoint['type'] == MessageType.TestStepFail:
            #         status_name = 'failed'
            #         break

        testcase_run_result.checkPoints = get_checkpoint_results()
        testcase_run_result.status = status_name

        update_result(testcase_run_result)


        # ExecutionMetaInfo().update_status(status_name)
        # FeatureOverView().update_status(status_name)

        # self.obj_scenario_meta_info.duration = scenario.duration * 1000
        # self.obj_scenario_meta_info.result = status_name

        # obj_meta_data = MetaData()
        # obj_meta_data.name = scenario.name
        # obj_meta_data.resultFileName = scenario.name
        # if scenario.description:
        #     obj_meta_data.description = scenario.description
        # obj_meta_data.referece = six.text_type(scenario.location)
        # obj_meta_data.groups = scenario.effective_tags
        #
        # self.obj_scenario_meta_info.metaData = obj_meta_data.to_json_dict()
        # self.obj_scenario_meta_info.close()
        #
        # del self.obj_scenario_meta_info
        # self.obj_scenario_meta_info = None
        # Scenario(file_name=scenario.name).seleniumLog = CommandLogStack().get_all_command_log()

    def before_step(self, context, step):
        self.current_step = step
        start_step(step.keyword + ' ' + step.name)
        #start_step("base environment")


    def after_step(self, context, step):
        status = step_status(step)
        b_status = bool(re.search('(?i)pass', status)) if bool(re.search('(?i)fail|pass', status)) else None
        end_step(b_status)
        # obj_step = Step()
        # obj_step.start_behave_step(step)
        # obj_step.stop_behave_step(step)
        # Scenario(file_name=self.current_scenario.name).add_checkPoints(obj_step.obj_check_point)
        # del obj_step
