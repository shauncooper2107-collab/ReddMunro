# Test counts

This is the only place the suite size is written down. The README, the
hand-off, the pre-launch checklist and the 0.1.2 notes point here. Each
suite checks its own row at the end of a run and exits non-zero if the
row is wrong, so a new check cannot ship while this file still quotes
the old number.

The figures are the full run: PyYAML installed, and `REDD_REQUIRE_EXTRAS=1`
for the engine (that is what CI sets). Without PyYAML the reference-scan
checks skip, the engine prints a smaller pass count, and that run is not
this table.

| Suite | Passed | Skipped |
|---|---|---|
| engine | 360 | 0 |
| backend | 108 | 0 |
| schemas | 17 | 0 |
| scale | 14 | 0 |
| **total** | **499** | |

Re-derive from the repo root:

```bash
REDD_REQUIRE_EXTRAS=1 python test_signal_audit.py
python backend/test_backend.py
python backend/test_schemas.py
python test_scale_basis.py
```

`backend/test_schemas.py` needs the server extra
(`pip install fastapi uvicorn python-multipart pydantic`).
`backend/test_backend.py` does not. A plain `pytest` at the repo root
runs all four and skips the schema suite when that extra is absent,
instead of dying while collecting it.
