import re
from dataclasses import dataclass, field
from typing import List
from typing import Union

import pytest
from _pytest import nodes

from qaf.automation.bdd2.bdd2parser import parse
from qaf.qaf_pytest_plugin import metadata

"""
@author: Chirag Jayswal
"""


# load_step_modules()
@dataclass
class Bdd2Step:
    _name: str
    line_number: int = 0
    keyword: str = ""

    def __init__(self, name: str, line_number: int = 0) -> None:
        self.name = name
        self.line_number = line_number

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        match = re.match(
            "|".join(["Given", "When", "Then", "And"])
            , value,
            re.I)
        self.keyword = match.group() if match else ""
        self._name = value.replace(self.keyword, "").strip()

    def __str__(self):
        return self.keyword + ' ' + self.name


@dataclass
class BDD2Scenario:
    name: str
    line_number: int
    steps: list[Bdd2Step] = field(default_factory=list)
    metadata: dict[str] = field(default_factory=dict)
    testdata: dict[str] = field(default_factory=dict)
    description: list[str] = field(default_factory=list)
    background = None
    is_dryrun_mode: bool = False

    @property
    def has_dataprovider(self):
        return "JSON_DATA_TABLE" in self.metadata or "datafile" in self.metadata

    def get_test_func(self):
        from qaf.automation.bdd2.bddstep_executor import execute_step
        if self.has_dataprovider:
            @metadata(**self.metadata)
            def test_secario(testdata):
                for bdd_step in self.steps.copy():
                    execute_step(bdd_step, testdata, self.is_dryrun_mode)

            return test_secario
        else:
            @metadata(**self.metadata)
            def test_secario():
                for bdd_step in self.steps.copy():
                    execute_step(bdd_step, {}, self.is_dryrun_mode)

            return test_secario


class BDD2File(pytest.Module):
    def collect(self):
        values: List[Union[nodes.Item, nodes.Collector]] = []
        self.scenarios = parse(self.path)

        is_dryrun_mode = self.config.getoption("--dryrun")
        dict_values: List[List[Union[nodes.Item, nodes.Collector]]] = []
        ihook = self.ihook
        for scenario in self.scenarios:
            self.obj = scenario
            scenario.is_dryrun_mode = is_dryrun_mode
            fun = scenario.get_test_func()
            setattr(scenario, scenario.name, fun)

            res = ihook.pytest_pycollect_makeitem(
                collector=self, name=scenario.name, obj=fun
            )
            if res is None:
                continue
            elif isinstance(res, list):
                values.extend(res)
            else:
                values.append(res)
        dict_values.append(values)
        # Between classes in the class hierarchy, reverse-MRO order -- nodes
        # inherited from base classes should come before subclasses.
        result = []
        for values in reversed(dict_values):
            result.extend(values)
        return result

    def istestfunction(self, obj: object, name: str) -> bool:
        return True
