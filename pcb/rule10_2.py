# -*- coding: utf-8 -*-

from rule import *

class Rule10_2(KLCRule):
    """
    Create the methods check and fix to use with the kicad_mod files.
    """
    def __init__(self, module):
        super(Rule10_2, self).__init__('Rule 10.2', 'Doc property contains a full description of footprint.')

    def check(self, module):
        """
        Proceeds the checking of the rule.
        """
        return True if not module.description else False

    def fix(self, module):
        """
        Proceeds the fixing of the rule, if possible.
        """
        if self.check(module):
            # Can't fix this one!
            pass
