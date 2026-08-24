# v0.1.2 — two first-command failures

```
pip install --upgrade redd-munro
```

**If you are on 0.1.0 or 0.1.1, upgrade.** Both of the bugs below stop
the tool on the first or second thing a new user types, and neither
announced itself.

Nothing about the audit changed. Same numbers, same findings, same
engine — 11 metrics on the shipped Prometheus corpus still carry 5.6
independent signals.

---

## Redirecting the output crashed

```
redd run board.csv > report.txt
```

On Windows a redirected stream uses the locale codepage rather than
UTF-8, and the report contains `█ ─ · ✓ ▲ ○ ×`. So this raised
`UnicodeEncodeError`, printed a traceback and produced no report.

Redirecting is roughly the second thing anyone types — it is how you send
output to a colleague — so this was reachable within a minute of
installing. Output now degrades to ASCII on any stream that cannot carry
the glyphs, verified against **cp1252, ascii, cp437 and utf-8**:

```
#################.................  49% redundant
```

Degrading a glyph is a rendering choice and touches no number, the same
trade the colour handling already makes when you pipe it. A test asserts
that *every* non-ASCII character the CLI emits has a fallback, so the
next one added cannot quietly reintroduce the crash.

## The package would not import on the Python it claimed to support

`pyproject.toml` declares `requires-python = ">=3.8"`. A PEP 604 union —
`lex: dict | None` — sat in a function annotation, which is evaluated at
import time, and raises `TypeError` on 3.8 and 3.9.

So on Ubuntu 20.04 or Debian 11 you could install the package cleanly,
type `redd`, and get a traceback. **CI had only ever run 3.11**, so
nothing here caught it.

Fixed, and the floor is now tested rather than asserted: CI runs a
**3.8 + 3.11 matrix**. If the floor job ever fails, the correct response
is to raise `requires-python`, not to delete the job. That is written in
the workflow beside the setting.

This is the same shape as the `int64` index that was free on x86-64 and
raised `TypeError` in every visitor's browser for five days while 134
tests passed — none of them on wasm32. **A platform claim that nothing
tests is not a claim.**

---

## Also in this release

- **A duplicate header name no longer deletes a column.** `cpu,cpu,mem`
  returned *two* metrics: the second `cpu` overwrote the first, nothing
  was reported, and the headline counted a number of metrics the file did
  not contain. Both columns are now kept, the second renamed by position,
  and the rename is reported. A dashboard that exports the same panel
  twice is redundancy — which is the thing this tool exists to find, so
  collapsing the pair destroyed the finding and its evidence together.
- **`redd run --worksheet` and `--refs` are refused instead of ignored.**
  They are honoured under `prune` only. Previously they were accepted,
  exited 0 and did nothing — which is how a command that cannot work
  ended up in the README and on the website. The error now reconstructs
  your command with `prune` substituted.
- **Refusals name the likely cause.** A long-format file
  (`timestamp,metric,value`) is told it is long format and given the
  one-line pivot; a semicolon file is told it is semicolon-delimited; a
  6-row file is told it has 6 rows rather than being blamed on its
  columns. A negative control asserts none of these fire on a healthy
  file — a parser that cries wolf trains people to ignore the one message
  that matters.
- **Worksheet triage tiers.** Rows are grouped by *what was checked* —
  `C - conflict`, `A - identity pair`, `B - high redundancy` — with the
  number of sources scanned inside the cell. Without `--refs` every tier
  reads `NO SCAN`, because "not found" means nothing when nothing was
  searched. **No tier asserts safety.** "Tier 1 (Zero-Risk)" was proposed
  and refused; a tier is an efficient way to smuggle a clearance into a
  document whose job is to withhold one.
- **Rollback headers** on generated artefacts. Shadow dashboards carry
  `RESTORE: nothing was modified…` in the Grafana `description` field;
  routing configs lead with `RESTORE: this file has not been applied to
  anything.` Neither invents a git command — this code does not know your
  repository, and a restore command that is wrong gets run under
  pressure.

## New in the record

- **`CONTROLLED_FLAT_PREREG.md`** — a metric held near-constant by a
  working control loop loses its unique variance and is offered for
  archiving, and it is the channel that moves first when that loop fails.
  Measured 0.90 → 0.0000 as the loop tightens. **Documented, not fixed**:
  a detector that has not been scored would be the false confidence this
  project exists to refuse.
- **`ADOPTION_PREREG.md`** — three predictions about where teams actually
  stall, registered before any team was contacted, including an
  amendment recording that publishing one of them on the website
  contaminates it.

Both unscored. So is `HISTORY_STORE_PREREG.md` **H1**, which is still the
thing this project most needs and cannot get alone: a window somebody
labelled `incident` because their service was genuinely broken.

**496 checks.** Apache 2.0. numpy only. Nothing is uploaded, asserted at
runtime.
