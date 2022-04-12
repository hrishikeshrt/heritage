#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Constants"""

###############################################################################

HERITAGE_LANG = {
    "gender": {
        "m": "पुंलिङ्गम्",
        "f": "स्त्रीलिङ्गम्",
        "n": "नपुंसकलिङ्गम्",
        "*": "त्रिलिङ्गम्",
    },
    "case": {
        "nom": "प्रथमा",
        "acc": "द्वितीया",
        "i": "तृतीया",
        "dat": "चतुर्थी",
        "abl": "पञ्चमी",
        "g": "षष्ठी",
        "loc": "सप्तमी",
        "voc": "सम्बोधनम्",
    },
    "number": {"sg": "एकवचनम्", "du": "द्विवचनम्", "pl": "बहुवचनम्"},
}

###############################################################################
# Semantics of Colours
# https://sanskrit.inria.fr/manual.html

HERITAGE_COLOURS = {
    "deep_sky": "substantive/adjective forms",  # सुभन्त
    "red": "finite verbal forms",  # तिङन्त
    "lawngreen": "vocative",
    "mauve": "indeclinable forms such as adverbs, conjunctions, prepositions",
    "light_blue": "pronominal forms",
    "yellow": "initial part of compounds",
    # Actually, complex compounds with n+1 components appear as a
    # sequence of n yellow segments denoting stems, followed by a blue
    # nominal inflected form.
    "cyan": "exocentric compound",  # बहुव्रीहि समास
    # The cyan colour segment may not occur stand-alone,
    # it is mandatorily preceded by a yellow segment in order to form
    # an exocentric adjectival compound
    "lavender": "first preposition of the compound",  # अव्ययीभाव
    "magenta": "invariable form in the compound",  # अव्ययीभाव
    # There exists yet another variety of compound, the so-called avyayībhāva
    # "turned into undeclinable".
    # e.g. निर्मक्षिकम्
    # Here this input is analysed as a sequence of segments,
    # first the preposition nis, colored lavender, and then the stem makṣikā,
    # turned into an invariable form makṣikam, colored magenta.
    "grey": "unrecognized",
    "orange": "initial part of verbal compounds in periphrastic construction",
    # Verbal compounds exist, such as the periphrastic perfect construction,
    # used for secondary conjugations and nominative verbs. It builds a
    # special stem in -आम्, suffixed by a perfect form of one of the
    # auxiliaries कृ, अस् and भू.
    # e.g. First part of कथयाञ्चक्रे
    # The orange and red segments are mutually linked, thus selecting one
    # selects automatically the other.
    # Another periphrastic construction is the inchoative "cvi" verbal
    # compound. Its left part is a special substantival stem in ī or ū, and
    # its right part a finite verb form of one of the auxiliaries.
    # e.g. First part of मृदूभवति , खिलीभूतः etc.
    # Here, the right part is either red for verbal forms, e.g मृदूभवति
    # blue for participial forms, like कदर्थीकृतः
    # or mauve for absolutives and infinitives, like निमित्तीकृत्य
    "carmin": "special infinitive form"
    # e.g. First part of वक्तुकामः
}

###############################################################################
