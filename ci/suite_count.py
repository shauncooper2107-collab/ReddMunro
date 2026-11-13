"""The suite sizes live in docs/TESTING.md and nowhere else.

Each suite calls check_suite() after its own checks, with the pass and
skip totals it just counted. A mismatch is a failed run, which is how
the number stays the number the tests actually produced.
"""

import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(_ROOT, "docs", "TESTING.md")
_ROW = re.compile(
    r"^\| (engine|backend|schemas|scale) \| (\d+) \| (\d+) \|", re.M)
_TOTAL = re.compile(r"^\| \*\*total\*\* \| \*\*(\d+)\*\* \|", re.M)


def table():
    text = open(DOC, encoding="utf-8").read()
    rows = {m.group(1): (int(m.group(2)), int(m.group(3)))
            for m in _ROW.finditer(text)}
    total = _TOTAL.search(text)
    return text, rows, int(total.group(1)) if total else None


def check_suite(name, passed, skipped=0):
    """Return an error string, or None when this run matches the file.

    A run that skipped checks (no PyYAML, and REDD_REQUIRE_EXTRAS unset)
    is not the run this file records, so it is not failed for the
    mismatch. CI sets the variable, and a fully installed run has zero
    skips, so both still have to match.
    """
    try:
        _text, rows, total = table()
    except OSError as exc:
        return f"docs/TESTING.md could not be read: {exc}"
    got = rows.get(name)
    full = os.environ.get("REDD_REQUIRE_EXTRAS") == "1" or skipped == 0
    if full and got != (passed, skipped):
        return (f"docs/TESTING.md says {name} is {got}, this run is "
                f"{passed} passed, {skipped} skipped. That file is the "
                f"only copy of the count — update it.")
    if name == "engine" and full and total is not None:
        summed = sum(p for p, _s in rows.values())
        if total != summed:
            return (f"docs/TESTING.md total is {total}, the rows sum to "
                    f"{summed}.")
    return None
