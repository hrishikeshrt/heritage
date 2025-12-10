#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Command line interface for Heritage.py."""

###############################################################################

from __future__ import annotations

import argparse
import json
import sys
import logging
from dataclasses import asdict, is_dataclass
from typing import Any, Dict

from . import Font, HeritagePlatform, Lexicon, Method, SandhiMode

###############################################################################


def dataclass_to_dict(obj: Any) -> Any:
    """Convert nested dataclasses into dictionaries."""
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, dict):
        return {k: dataclass_to_dict(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [dataclass_to_dict(v) for v in obj]
    return obj


def build_platform(args: argparse.Namespace) -> HeritagePlatform:
    """Create a configured HeritagePlatform instance from CLI arguments."""
    platform_kwargs: Dict[str, Any] = {}
    if args.base_dir:
        platform_kwargs["base_dir"] = args.base_dir
    if args.base_url:
        platform_kwargs["base_url"] = args.base_url
    if args.request_timeout is not None:
        platform_kwargs["request_timeout"] = args.request_timeout
    if args.request_attempts is not None:
        platform_kwargs["request_attempts"] = args.request_attempts

    platform = HeritagePlatform(method=args.method.value, **platform_kwargs)

    if args.lexicon:
        platform.set_lexicon(args.lexicon.value)
    if args.font:
        platform.set_font(args.font.value)

    return platform


def configure_parser() -> argparse.ArgumentParser:
    """Configure the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="heritage",
        description="Interact with the Sanskrit Heritage Platform.",
    )
    parser.add_argument(
        "--method",
        choices=list(Method),
        type=Method,
        default=Method.WEB,
        help="Backend to use (web mirror or local shell executables).",
    )
    parser.add_argument(
        "--base-dir",
        help="Path to the local Heritage_Platform checkout (shell mode).",
    )
    parser.add_argument(
        "--base-url",
        help="Alternative web mirror base URL.",
    )
    parser.add_argument(
        "--lexicon",
        choices=list(Lexicon),
        type=Lexicon,
        help="Preferred lexicon for queries (defaults to MW).",
    )
    parser.add_argument(
        "--font",
        choices=list(Font),
        type=Font,
        help="Output font preference for Sanskrit text.",
    )
    parser.add_argument(
        "--request-timeout",
        type=int,
        help="HTTP timeout (seconds) when using web mode.",
    )
    parser.add_argument(
        "--request-attempts",
        type=int,
        help="Number of HTTP retry attempts when using web mode.",
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Reduce logging noise (warnings and errors only).",
    )
    verbosity.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Increase logging verbosity (debug output).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Analysis -----------------------------------------------------------------
    analysis_parser = subparsers.add_parser(
        "analysis", help="Obtain morphological analyses for a sentence/word."
    )
    analysis_parser.add_argument("text", help="Input text in Devanagari.")
    analysis_parser.add_argument(
        "--word",
        action="store_true",
        help="Treat input as a single word (disable sentence mode).",
    )
    analysis_parser.add_argument(
        "--unsandhied",
        action="store_true",
        help="Mark the input as already unsandhied.",
    )
    analysis_parser.add_argument(
        "--meta",
        action="store_true",
        help="Include parser options metadata in the response.",
    )
    analysis_parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of human-readable text.",
    )

    # Parse --------------------------------------------------------------------
    parse_parser = subparsers.add_parser(
        "parse", help="Fetch semantic roles for a previously analysed sentence."
    )
    parse_parser.add_argument("text", help="Input text in Devanagari.")
    parse_parser.add_argument(
        "--solution-id",
        type=int,
        help="Solution ID to resolve. Defaults to the first solution.",
    )
    parse_parser.add_argument(
        "--json", action="store_true", help="Output JSON."
    )

    # Declension ---------------------------------------------------------------
    decl_parser = subparsers.add_parser(
        "declension", help="Retrieve declension tables for a noun."
    )
    decl_parser.add_argument("word", help="Word in Devanagari.")
    decl_parser.add_argument(
        "--gender",
        required=True,
        help="Gender hint (m/f/n, Mas/Fem/Neu).",
    )
    decl_parser.add_argument(
        "--json", action="store_true", help="Output JSON."
    )

    # Conjugation --------------------------------------------------------------
    conj_parser = subparsers.add_parser(
        "conjugation", help="Retrieve conjugation paradigms for a verb."
    )
    conj_parser.add_argument("word", help="Root in Devanagari.")
    conj_parser.add_argument(
        "--gana",
        required=True,
        help="Verbal class (gana) required by the grammarian.",
    )
    conj_parser.add_argument(
        "--json", action="store_true", help="Output JSON."
    )

    # Sandhi -------------------------------------------------------------------
    sandhi_parser = subparsers.add_parser(
        "sandhi", help="Form sandhi between two words."
    )
    sandhi_parser.add_argument("left", help="Left word.")
    sandhi_parser.add_argument("right", help="Right word.")
    sandhi_parser.add_argument(
        "--mode",
        choices=list(SandhiMode),
        type=SandhiMode,
        default=SandhiMode.INTERNAL,
        help="Sandhi mode (internal/external).",
    )

    # Search -------------------------------------------------------------------
    search_parser = subparsers.add_parser(
        "search", help="Search the lexicon for a word."
    )
    search_parser.add_argument("word", help="Word in Devanagari.")
    search_parser.add_argument(
        "--json", action="store_true", help="Output JSON."
    )

    return parser


def cmd_analysis(args: argparse.Namespace, platform: HeritagePlatform) -> int:
    sentence = not args.word
    solutions = platform.get_analysis(
        args.text, sentence=sentence, unsandhied=args.unsandhied, meta=args.meta
    )
    if solutions is None:
        print("No analysis available.", file=sys.stderr)
        return 1
    payload = {idx: dataclass_to_dict(sol) for idx, sol in solutions.items()}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    for solution_id in sorted(solutions):
        solution = solutions[solution_id]
        print(f"Solution {solution.id}")
        for word in solution.words:
            print(f"  {word.text}")
            for candidate in word.candidates:
                analyses = ", ".join(" ".join(a) for a in candidate.analyses)
                print(f"    - {candidate.root}: {analyses}")
        if solution.parser_options:
            print(f"    options: {solution.parser_options}")
    return 0


def cmd_parse(args: argparse.Namespace, platform: HeritagePlatform) -> int:
    solution = platform.get_parse(
        args.text, solution_id=args.solution_id, sentence=True
    )
    if solution is None:
        print("Unable to retrieve parse.", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(dataclass_to_dict(solution), ensure_ascii=False, indent=2))
        return 0
    print(f"Solution {solution.id}")
    if solution.roles:
        for role in solution.roles:
            print(f"  {role.text}: {', '.join(role.roles)}")
    else:
        print("  No roles available.")
    return 0


def cmd_declension(args: argparse.Namespace, platform: HeritagePlatform) -> int:
    table = platform.get_declensions(
        args.word, gender=args.gender, structured=True
    )
    if table is None:
        print("Unable to retrieve declension table.", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(dataclass_to_dict(table), ensure_ascii=False, indent=2))
        return 0
    if table.headers:
        print("\t".join(table.headers))
    for row in table.rows:
        print("\t".join(row))
    return 0


def cmd_conjugation(args: argparse.Namespace, platform: HeritagePlatform) -> int:
    tables = platform.get_conjugations(
        args.word, gana=args.gana, structured=True
    )
    if tables is None:
        print("Unable to retrieve conjugation data.", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(dataclass_to_dict(tables), ensure_ascii=False, indent=2))
        return 0
    for table in tables:
        print(table.title)
        for cell in table.cells:
            print(f"  {cell.heading}")
            for row in cell.rows:
                print("    " + "\t".join(row))
    return 0


def cmd_sandhi(args: argparse.Namespace, platform: HeritagePlatform) -> int:
    result = platform.sandhi(args.left, args.right, mode=args.mode.value)
    if result is None:
        print("Sandhi calculation failed.", file=sys.stderr)
        return 1
    print(result)
    return 0


def cmd_search(args: argparse.Namespace, platform: HeritagePlatform) -> int:
    results = platform.search_lexicon(args.word, structured=True)
    if not results:
        print("No results.", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(dataclass_to_dict(results), ensure_ascii=False, indent=2))
        return 0
    for result in results:
        link = f" ({result.link})" if result.link else ""
        summary = f" – {result.summary}" if result.summary else ""
        print(f"{result.entry}{link}{summary}")
    return 0


def main() -> int:
    """Entry point for the CLI."""
    parser = configure_parser()
    args = parser.parse_args()

    level = logging.INFO
    if getattr(args, "quiet", False):
        level = logging.WARNING
    elif getattr(args, "verbose", False):
        level = logging.DEBUG

    logging.basicConfig(
        format="[%(asctime)s] %(name)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level,
    )

    platform = build_platform(args)

    command_map = {
        "analysis": cmd_analysis,
        "parse": cmd_parse,
        "declension": cmd_declension,
        "conjugation": cmd_conjugation,
        "sandhi": cmd_sandhi,
        "search": cmd_search,
    }

    handler = command_map.get(args.command)
    if handler is None:
        parser.print_help()
        return 1
    return handler(args, platform)


###############################################################################


if __name__ == "__main__":
    raise SystemExit(main())
