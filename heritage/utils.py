#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utility Functions"""

###############################################################################

from urllib.parse import urlencode


def build_query_string(options: dict) -> str:
    """
    Build a CGI-compatible ``QUERY_STRING``.

    Values set to ``None`` are dropped and literal ``+`` characters are kept
    intact because the Heritage CGI scripts rely on plus-separated tokens for
    multi-word inputs.
    """
    filtered = {k: v for k, v in options.items() if v is not None}
    return urlencode(filtered, doseq=True, safe="+")


###############################################################################


def devanagari_to_velthuis(text: str) -> str:
    """
    Convert Devanagari text to Velthuis

    Heritage Platform uses its own DN to VH conversion
    This deviates from the standard one (from Wiki or other sources)
    Following is a translation of the JS function convert() from the
    Heritage Platform
    Source URL: https://sanskrit.inria.fr/DICO/utf82VH.js
    """

    inHex = [
        "05",
        "06",
        "07",
        "08",
        "09",
        "0a",
        "0b",
        "60",
        "0c",
        "0f",
        "10",
        "13",
        "14",
        "02",
        "01",
        "03",
        "3d",
        "4d",
    ]
    outVH = [
        "a",
        "aa",
        "i",
        "ii",
        "u",
        "uu",
        ".r",
        ".rr",
        ".l",
        "e",
        "ai",
        "o",
        "au",
        ".m",
        "~l",
        ".h",
        "'",
        "",
    ]
    matIn = [
        "3e",
        "3f",
        "40",
        "41",
        "42",
        "43",
        "44",
        "62",
        "47",
        "48",
        "4b",
        "4c",
    ]
    consIn = [
        "15",
        "16",
        "17",
        "18",
        "19",
        "1a",
        "1b",
        "1c",
        "1d",
        "1e",
        "1f",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "2a",
        "2b",
        "2c",
        "2d",
        "2e",
        "2f",
        "30",
        "32",
        "35",
        "36",
        "37",
        "38",
        "39",
        "00",
    ]

    orig = text
    output = ""
    wasCons = False

    for i in range(len(orig)):
        origC = orig[i]
        hexcode = hex(ord(origC)).lstrip("0x")
        lenL = len(hexcode)
        hexcode = "0" * (4 - lenL) + hexcode

        check = hexcode[2:]
        init = hexcode[:2]

        if init != "09":
            check = "00"
        consOut = [
            "k",
            "kh",
            "g",
            "gh",
            "f",
            "c",
            "ch",
            "j",
            "jh",
            "~n",
            ".t",
            ".th",
            ".d",
            ".dh",
            ".n",
            "t",
            "th",
            "d",
            "dh",
            "n",
            "p",
            "ph",
            "b",
            "bh",
            "m",
            "y",
            "r",
            "l",
            "v",
            "z",
            ".s",
            "s",
            "h",
            origC + "",
        ]

        for j in range(len(inHex)):
            if check == inHex[j]:
                if check in ["01", "02", "03", "3d"]:
                    if wasCons:
                        output += "a" + outVH[j]
                    else:
                        output += outVH[j]
                else:
                    output += outVH[j]
                wasCons = False

        for j in range(len(consIn)):
            if check == consIn[j]:
                if wasCons:
                    output += "a" + consOut[j]
                else:
                    output += consOut[j]
                wasCons = check != "00"
                if i == len(orig) - 1:
                    output += "a"
        for j in range(len(matIn)):
            if check == matIn[j]:
                output += outVH[j + 1]
                wasCons = False

    return output
