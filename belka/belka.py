#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Belka

    (c) ken pepple (ken@pepple.info)

"""

import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class BelkaApp(App):

    log = logging.getLogger(__name__)

    def __init__(self):
        super(BelkaApp, self).__init__(
            description='belka',
            version='0.2.4',
            command_manager=CommandManager('cliff.belka'),
        )

    def initialize_app(self, argv):
        self.log.debug('initialize_app')
        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.WARNING)

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = BelkaApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
