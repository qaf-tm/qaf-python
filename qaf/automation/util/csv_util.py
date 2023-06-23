# -*- coding: utf-8 -*-
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

# @Author: Chirag Jayswal
# module settings
__version__ = '1.0.0'
__all__ = [
    'get_csvdata_as_map',
]

import ast
import csv


def get_csvdata_as_map(csvfile):
    rows = []
    with open(csvfile, encoding='utf-8') as csvf:
        # return get_list_of_map(csvf)
        #there can be inital commented lines
        #csv_data = [line.strip('\n') for line in csvf]
        csv_data = filter(lambda row: row.strip() and row.strip()[0]!='#', csvf)
        return get_list_of_map(csv_data)


def get_list_of_map(csv_data, delimiter=","):
    rows = []
    csvReader = csv.DictReader(csv_data, delimiter=delimiter, skipinitialspace=True)
    for row in csvReader:
        first_key = next(iter(row))
        if not row[first_key].startswith("#"):
            for key, val in row.items():
                try:
                    row[key] = ast.literal_eval(val)
                except:
                    pass
            rows.append(row)
    return rows