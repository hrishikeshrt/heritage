#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Console script for Heritage."""

###############################################################################

import os
import sys
import argparse

from . import HeritagePlatform

###############################################################################


def main():
    """Console script for Heritage.py"""
    home_dir = os.path.expanduser("~")
    heritage_dir = os.path.join(
        home_dir, "git", "heritage", "Heritage_Platform"
    )
    SH = HeritagePlatform(heritage_dir)  # noqa

    parser = argparse.ArgumentParser(
        description="Console Script for Heritage.py"
    )
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into heritage.cli.main")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
