# SPDX-License-Identifier: GPL-2.0

"""
Show status of DAMON.
"""

import json
import random
import time

import _damo_fmt_str
import _damon
import _damon_args

def update_pr_schemes_stats(json_format, raw_nr):
    err = _damon.update_schemes_stats()
    if err:
        print(err)
        return
    kdamonds = _damon.current_kdamonds()

    kvpairs = []
    for kd_idx, kdamond in enumerate(kdamonds):
        kvpairs.append([])
        for ctx_idx, ctx in enumerate(kdamond.contexts):
            kvpairs[-1].append([])
            for scheme_idx, scheme in enumerate(ctx.schemes):
                kvpairs[-1][-1].append(scheme.stats.to_kvpairs(raw_nr))
                if not json_format:
                    print('kdamond %s context %s scheme %s' %
                            (kd_idx, ctx_idx, scheme_idx))
                    print(scheme.stats.to_str(raw_nr))

    if not json_format:
        return
    print(json.dumps(kvpairs, indent=4))

def pr_kdamonds_summary(json_format, raw_nr):
    kdamonds = _damon.current_kdamonds()
    summary = [k.summary_str() for k in kdamonds]
    if json_format:
        print(json.dumps(summary, indent=4))
        return
    if len(summary) == 1:
        print(summary)
    for idx, line in enumerate(summary):
        print('%d\t%s' % (idx, line))

def pr_kdamonds(kdamonds, json_format, raw_nr, damos_stat_indices,
        damos_stat_field):
    if damos_stat_indices:
        kidx, cidx, sidx = damos_stat_indices
        if kidx >= len(kdamonds):
            print('too high kdamond index')
            exit(1)
        kdamond = kdamonds[kidx]
        if cidx >= len(kdamond.contexts):
            print('too high context index')
            exit(1)
        ctx = kdamond.contexts[cidx]
        if sidx >= len(ctx.schemes):
            print('too high scheme index')
            exit(1)
        scheme = ctx.schemes[sidx]

        if damos_stat_field != None:
            kvpairs = scheme.stats.to_kvpairs(raw_nr)
            if not damos_stat_field in kvpairs:
                print('wrong damos_stat_field')
                exit(1)
            print(kvpairs[damos_stat_field])
            return

        if json_format:
            print(json.dumps(scheme.stats.to_kvpairs(raw_nr), indent=4))
        else:
            print(scheme.stats.to_str(raw_nr))
        return

    if json_format:
        print(json.dumps([k.to_kvpairs(raw_nr) for k in kdamonds], indent=4))
    else:
        for idx, k in enumerate(kdamonds):
            print('kdamond %d' % idx)
            print(_damo_fmt_str.indent_lines( k.to_str(raw_nr), 4))


def set_argparser(parser):
    parser.add_argument('--json', action='store_true', default=False,
            help='print output in json format')
    parser.add_argument('--raw', action='store_true', default=False,
            help='print raw numbers')
    parser.add_argument('--kdamonds_summary', action='store_true',
            help='print kdamond summary only')
    parser.add_argument('--damos_stats', action='store_true',
            help='print DAMOS scheme stats only')
    parser.add_argument('--damos_stat', nargs=3, type=int,
            metavar=('<kdamond index>', '<context index>', '<scheme index>'),
            help='print statistics of specific scheme')
    parser.add_argument('--damos_stat_field',
            metavar='<stat field name>',
            help='statistic field to show, if --damos_stat is given')
    _damon_args.set_common_argparser(parser)
    return parser

def main(args=None):
    if not args:
        parser = set_argparser(parser)
        args = parser.parse_args()

    _damon.ensure_root_and_initialized(args)
    # ignore the error.  status could be called before feature saving commands.
    err = _damon.read_feature_supports_file()

    if args.kdamonds_summary:
        return pr_kdamonds_summary(args.json, args.raw)

    if args.damos_stats:
        return update_pr_schemes_stats(args.json, args.raw)

    kdamonds, err = _damon.update_read_kdamonds(nr_retries=5,
            update_stats=True,
            update_tried_regions=(args.damos_stat == None))
    if err != None:
        print('cannot update and read kdamonds: %s' % err)
        exit(1)
    pr_kdamonds(kdamonds, args.json, args.raw, args.damos_stat,
            args.damos_stat_field)

if __name__ == '__main__':
    main()
