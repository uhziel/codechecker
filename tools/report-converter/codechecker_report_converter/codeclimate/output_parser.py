# -------------------------------------------------------------------------
#
#  Part of the CodeChecker project, under the Apache License v2.0 with
#  LLVM Exceptions. See LICENSE for license information.
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
# -------------------------------------------------------------------------

import logging
import os
import json

from ..output_parser import BaseParser, Message, Event

LOG = logging.getLogger('ReportConverter')

def _get_begin_line(location):
    if 'lines' in location:
        return location['lines']['begin']
    elif 'positions' in location:
        if 'begin' in location['positions']:
            return location['positions']['begin']['line']
    else:
        return 0

class CodeClimateParser(BaseParser):
    """ Parser for CodeClimate output. """

    def __init__(self):
        super(CodeClimateParser, self).__init__()

    def parse_messages(self, analyzer_result):
        """ Parse the given analyzer result. """

        with open(analyzer_result) as f:
            for l in f:
                error = json.loads(l.rstrip('\0\n'))
                message = self.__parse_error(error)
                if message:
                    self.messages.append(message)

        return self.messages

    def __parse_error(self, error):
        """ Parse the given error and create a message from them. """

        location = error['location']
        file_path = location['path']
        line = int(_get_begin_line(location))
        column = 0
        msg = error['description']
        if 'severity' in error:
            checker_name = error['severity'] + "." + error['check_name']
        else:
            checker_name = error['check_name']
        
        events = [Event(file_path, line, column, msg)]

        if 'other_locations' in error:
           for loc in error['other_locations']:
               events.append(Event(loc['path'], int(_get_begin_line(loc)), column, ''))

        message = Message(
            file_path,
            line,
            column,
            msg,
            checker_name,
            events)

        return message
