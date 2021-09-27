# -------------------------------------------------------------------------
#
#  Part of the CodeChecker project, under the Apache License v2.0 with
#  LLVM Exceptions. See LICENSE for license information.
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
# -------------------------------------------------------------------------

from codechecker_report_converter.analyzer_result import AnalyzerResult

from .output_parser import CodeClimateParser
from ..plist_converter import PlistConverter


class CodeClimateAnalyzerResult(AnalyzerResult):
    """ Transform analyzer result of CodeClimate. """

    TOOL_NAME = 'codeclimate'
    NAME = 'codeclimate'
    URL = 'https://github.com/codeclimate/platform/blob/master/spec/analyzers/SPEC.md#data-types'

    def parse(self, analyzer_result):
        """ Creates plist files from the given analyzer result to the given
        output directory.
        """
        parser = CodeClimateParser()
        messages = parser.parse_messages(analyzer_result)
        if not messages:
            return None

        plist_converter = PlistConverter(self.TOOL_NAME)
        plist_converter.add_messages(messages)
        return plist_converter.get_plist_results()
