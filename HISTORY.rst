History
=======

1.0.0 (2025-12-10)
------------------

* Make structured dataclasses the default return type for high-level helpers,
  including analyses, parses, declensions, conjugations, and lexicon searches.
* Add a `heritage.models` module with typed representations for solutions,
  tables, and dictionary/search results, and re-export them from the top-level
  package.
* Replace the placeholder console script with a real `heritage` CLI that
  exposes analysis, parse, declension, conjugation, sandhi, and search
  subcommands, supports `--json`, and adds `--quiet` / `--verbose` flags.
* Improve HTTP handling with configurable timeouts and retry counts, an
  exponential-backoff strategy, and more robust response decoding.
* Refine shell mode by preserving the ambient environment, using subprocess
  timeouts instead of process-wide signal handlers, and returning `None` on
  execution failure instead of raising low-level errors.
* Parse dictionary search results and single lexicon entries into structured
  objects instead of exposing raw HTML, with clearer logging when upstream
  responses are incomplete or malformed.
* Add tests that exercise HTML parsing helpers and core utilities to guard
  against regressions as the upstream Sanskrit Heritage site evolves.

0.1.0 (2022-03-23)
------------------

* First release on PyPI.
