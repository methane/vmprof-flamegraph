#!/usr/bin/env python3
from __future__ import absolute_import

import argparse
import os
import sys
import vmprof


class FlameGraphPrinter:
    """
    The Flame Graph [1] printer for vmprof profile files.

    [1] http://www.brendangregg.com/FlameGraphs/cpuflamegraphs.html
    """

    def __init__(self, prune_percent=0.1, prune_level=None):
        # (float, Optional[float]) -> None
        """
        :param prune_level: Prune output of a profile stats node when the node is deeper
            than this level down the call graph from the very top.
        """
        assert 0 <= prune_percent <= 100
        assert prune_level is None or (0 <= prune_level <= 900)
        self._prune_percent = prune_percent or 0.1
        self._prune_level = prune_level or 900

    def show(self, profile):
        # (str) -> None
        """Read and display a vmprof profile file.

        :param profile: The filename of the vmprof profile file to convert.
        """
        try:
            stats = vmprof.read_profile(profile)
        except Exception as e:
            print("Fatal: could not read vmprof profile file '{}': {}".format(profile, e),
                  file=sys.stderr)
            return
        tree = stats.get_tree()
        self.print_tree(tree)

    def _walk_tree(self, parent, node, level, lines):
        if ':' in node.name:
            block_type, funcname, *rest = node.name.split(':')
            if len(rest) >= 2:
                lineno = rest[0]
                filename = rest[1].split('/')[-1]
                funcname += ":{}:{}".format(filename, lineno)
            if parent:
                current = parent + ';' +funcname
            else:
                current = funcname
        else:
            current = node.name

        count = node.count

        level += 1
        if level <= self._prune_level:
            for c in node.children.values():
                if c.count >= self._minimum_count:
                    count -= c.count
                    self._walk_tree(current, c, level, lines)

        lines.append((current, count))

    def print_tree(self, tree):
        total = float(tree.count)
        self._minimum_count = total * self._prune_percent / 100.0
        lines = []
        self._walk_tree(None, tree, 0, lines)
        lines.sort()
        for p, c in lines:
            print(p, c)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("profile")
    parser.add_argument(
        '--prune_level',
        type=int,
        default=None,
        help='Prune output of a profile stats deeper than specified level.')
    parser.add_argument(
        '--prune_percent',
        type=float,
        default=0.1,
        help='Prune output of a profile stats less than specified percent.')
    args = parser.parse_args()

    pp = FlameGraphPrinter(args.prune_percent, args.prune_level)
    pp.show(args.profile)


if __name__ == '__main__':
    main()
