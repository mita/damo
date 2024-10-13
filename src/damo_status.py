# SPDX-License-Identifier: GPL-2.0

"""
Show status of DAMON.
"""

import damo_report_kdamonds

def main(args):
    '''
    'damo status' will be deprecated in favor of 'damo report kdamonds'.  To
    avoid unnecessary changes to 'damo_status.py' before it is officially
    deprecated and removed, make this source file to work as just a wrapper of
    'damo_report_kdamonds.py'.

    Another appraoch would be simply removing this file and updating 'damo.py'
    to keep 'status' command, but link 'damo_report_kdamodsn.py' file.  We
    don't use the approach to keep this file as a place to add deprecation
    message later.
    '''
    return damo_report_kdamonds.main(args)

def set_argparser(parser):
    return damo_report_kdamonds.set_argparser(parser)
