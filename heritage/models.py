#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Typed models used by the Heritage Platform wrapper."""

from __future__ import annotations

###############################################################################

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Sequence, Tuple


class Method(str, Enum):
    """Execution backend for the Heritage Platform."""

    SHELL = "shell"
    WEB = "web"


class Lexicon(str, Enum):
    """Available dictionary backends."""

    MW = "MW"
    SH = "SH"


class Font(str, Enum):
    """Output font options understood by the CGI scripts."""

    DEVA = "deva"
    ROMA = "roma"


class SandhiMode(str, Enum):
    """Modes supported by the sandhi engine."""

    INTERNAL = "internal"
    EXTERNAL = "external"


###############################################################################
# Morphological analysis models


@dataclass
class AnalysisCandidate:
    """Single candidate returned by the Reader Companion."""

    root: str
    analyses: List[List[str]]
    lexicon_reference: Optional[Tuple[Optional[str], Optional[str]]] = None


@dataclass
class WordAnalysis:
    """Analysis for a single word/token."""

    text: str
    category: List[Optional[str]] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    candidates: List[AnalysisCandidate] = field(default_factory=list)


@dataclass
class SolutionAnalysis:
    """Full solution comprising analyses for each token."""

    id: int
    words: List[WordAnalysis]
    parser_options: Optional[Dict[str, str]] = None
    roles: Optional[List["WordRole"]] = None


@dataclass
class WordRole:
    """Semantic role assignment extracted from the Reader Assistant."""

    text: str
    roles: List[str]


###############################################################################
# Tables


@dataclass
class DeclensionTable:
    """Declension grid produced by the grammarian."""

    headers: Sequence[str]
    rows: Sequence[Sequence[str]]


@dataclass
class ConjugationCell:
    """Single cell produced inside a conjugation table."""

    heading: str
    rows: Sequence[Sequence[str]]


@dataclass
class ConjugationTable:
    """Grouping for conjugation paradigms."""

    title: str
    cells: Sequence[ConjugationCell]


###############################################################################
# Dictionary and search


@dataclass
class DictionaryEntry:
    """Dictionary entry extracted from the Heritage lexicons."""

    lemma: str
    html: str
    text: str


@dataclass
class SearchResult:
    """Single row returned by the lexicon search interface."""

    entry: str
    link: Optional[str]
    summary: str

