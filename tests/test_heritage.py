#!/usr/bin/env python

"""Tests for the `heritage` package."""

from heritage.heritage import HeritageOutput
from heritage.models import ConjugationTable, DeclensionTable, DictionaryEntry, SearchResult
from heritage.utils import build_query_string, devanagari_to_velthuis


def test_build_query_string_filters_none_and_preserves_plus():
    options = {
        "lex": "MW",
        "cache": None,
        "text": "रामः+वनं",
    }
    qs = build_query_string(options)
    assert "cache=" not in qs
    assert "text=" in qs
    # Plus signs are significant for the upstream CGI scripts and must survive.
    assert "%2B" not in qs
    assert "+" in qs.split("text=", 1)[1]


def test_devanagari_to_velthuis_basic_vowels_and_consonant():
    # अ आ इ उ क -> a, aa, i, u, k
    assert devanagari_to_velthuis("अ") == "a"
    assert devanagari_to_velthuis("आ") == "aa"
    assert devanagari_to_velthuis("इ") == "i"
    assert devanagari_to_velthuis("उ") == "u"
    assert devanagari_to_velthuis("क") == "ka"


def test_extract_lexicon_entry_with_direct_lemma():
    html = """
    <html>
      <head>
        <title>Monier-Williams Sanskrit-English Dictionary</title>
      </head>
      <body>
        <span><a name="rama">राम</a> some definition text</span>
      </body>
    </html>
    """
    output = HeritageOutput(html)
    entry = output.extract_lexicon_entry("rama")
    assert isinstance(entry, DictionaryEntry)
    assert entry.lemma == "राम"
    assert "some definition text" in entry.text


def test_extract_lexicon_entry_falls_back_to_italic():
    html = """
    <html>
      <head>
        <title>Monier-Williams Sanskrit-English Dictionary</title>
      </head>
      <body>
        <span><a name="id"></a> <i>lemma-fallback</i> definition</span>
      </body>
    </html>
    """
    output = HeritageOutput(html)
    entry = output.extract_lexicon_entry("id")
    assert isinstance(entry, DictionaryEntry)
    assert entry.lemma == "lemma-fallback"
    assert "definition" in entry.text


def test_extract_lexicon_entry_invalid_title_or_id_returns_none():
    bad_title_html = """
    <html>
      <head><title>Not a dictionary page</title></head>
      <body><span><a name="id">x</a></span></body>
    </html>
    """
    output = HeritageOutput(bad_title_html)
    assert output.extract_lexicon_entry("id") is None

    missing_id_html = """
    <html>
      <head>
        <title>Monier-Williams Sanskrit-English Dictionary</title>
      </head>
      <body><span><a name="other">x</a></span></body>
    </html>
    """
    output = HeritageOutput(missing_id_html)
    assert output.extract_lexicon_entry("id") is None


def test_extract_search_results_structured_and_legacy():
    html = """
    <html>
      <head><title>Search Results</title></head>
      <body>
        <table>
          <tr>
            <td><a href="foo.html#1">रामः</a></td>
            <td>masculine noun</td>
          </tr>
          <tr>
            <td>वनम्</td>
            <td>neuter noun</td>
          </tr>
        </table>
      </body>
    </html>
    """
    output = HeritageOutput(html)

    structured = output.extract_search_results(structured=True)
    assert isinstance(structured, list)
    assert len(structured) == 2
    assert all(isinstance(item, SearchResult) for item in structured)
    assert structured[0].entry == "रामः"
    assert structured[0].link == "foo.html#1"
    assert "masculine noun" in structured[0].summary

    legacy = output.extract_search_results(structured=False)
    assert isinstance(legacy, list)
    assert legacy[1]["entry"] == "वनम्"
    assert legacy[1]["link"] is None
    assert "neuter noun" in legacy[1]["summary"]


def test_extract_declensions_structured_and_raw():
    html = """
    <html>
      <head><title>Sanskrit Grammarian Declension Engine</title></head>
      <body>
        <table class="inflexion">
          <tr><th>case</th><th>sg</th></tr>
          <tr><th>nom</th><th>रामः</th></tr>
          <tr><th>acc</th><th>रामम्</th></tr>
          <tr><th>loc</th><th>रामे</th></tr>
        </table>
      </body>
    </html>
    """
    output = HeritageOutput(html)
    table = output.extract_declensions(structured=True)
    assert isinstance(table, DeclensionTable)
    assert table.headers == ["case", "sg"]
    assert len(table.rows) == 3

    raw = output.extract_declensions(headers=False, structured=False)
    assert isinstance(raw, list)
    assert len(raw) == 3
    # Each row should contain the form column only.
    assert raw[0][0][0] == "रामः"
    assert raw[1][0][0] == "रामे"
    assert raw[2][0][0] == "रामम्"


def test_extract_conjugations_structured_and_raw():
    html = """
    <html>
      <head><title>Sanskrit Grammarian Conjugation Engine</title></head>
      <body>
        <table class="gris_cent">
          <tr><td><span>लट्</span></td></tr>
          <tr>
            <td>
              <table class="inflexion">
                <tr><th>परस्मैपदम्</th><th>एकवचनम्</th></tr>
                <tr><th>प्रथमपुरुषः</th><th>गच्छति</th></tr>
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """
    output = HeritageOutput(html)

    structured = output.extract_conjugations(structured=True)
    assert isinstance(structured, list)
    assert len(structured) == 1
    table = structured[0]
    assert isinstance(table, ConjugationTable)
    assert table.title == "लट्"
    assert len(table.cells) == 1
    cell = table.cells[0]
    assert cell.rows[0][0] == "प्रथमपुरुषः"
    assert cell.rows[0][1] == "गच्छति"

    legacy = output.extract_conjugations(structured=False)
    assert isinstance(legacy, dict)
    assert "लट्" in legacy
