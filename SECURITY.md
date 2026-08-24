# Security

## Reporting

**shaun@reddmunro.com.** Please do not open a public issue for a
vulnerability. There is no bug bounty and no formal SLA — this is one
person — but you will get a reply, and if the report is valid it will be
fixed and credited unless you would rather not be.

## Supported versions

| Version | Supported |
|---|---|
| 0.1.2 | yes |
| 0.1.1 | no — upgrade |
| 0.1.0 | no — upgrade |

`0.1.0` and `0.1.1` both accept `--worksheet` on `redd run`, exit 0 and
produce nothing. `0.1.0` and `0.1.1` also crash on a non-UTF-8 stream and
fail to import on Python 3.8 and 3.9. Neither is a security defect, but
neither should be in use.

## The threat model, stated plainly

**This tool reads your telemetry.** That is the whole point, and it is
worth being precise about what happens to it.

- **Nothing is uploaded, ever.** There is no network code in any shipped
  module. This is asserted twice in the test suite: statically, by
  scanning every shipped module for socket, urllib, requests, httpx and
  http.client; and at runtime, by replacing `socket.socket`,
  `create_connection` and `getaddrinfo` with a raiser and running five
  real CLI paths through the block. A positive control proves the block
  is armed first, so the assertions cannot pass vacuously.
- **The browser version is the same claim.** `reddmunro.com` runs the
  engine in your tab via WebAssembly. Open the network panel and check —
  after the initial asset load there is no request.
- **The tool writes files where you tell it.** `--html`, `--json`,
  `--worksheet`, `--shadow`, `--route` and `--record` all write to paths
  you supply. `--record` writes to `./.redd/`.
- **It never applies anything.** Routing configs and shadow dashboards
  are files. Applying them is your step, deliberately.

## What a generated artefact may contain

Worksheets, JSON, HTML reports, routing configs and shadow dashboards
**contain your metric names**, and the reference scan additionally
embeds **alert rule names and dashboard titles** it found. Metric names
leak architecture. Treat these outputs as you would treat the dashboard
export itself, and check before pasting one into a public issue.

## Do not deploy the backend

`backend/` is functionally complete and **must not be exposed**:

- authentication is a stub
- there is no persistence
- `InMemoryJobStore` breaks behind more than one worker

All three refuse or warn rather than failing quietly, and
`SIGNAL_AUDIT_REQUIRE_AUTH=1` exists, but the correct action today is not
to run it. Nothing in the published package starts a server.

## Dependencies

`numpy` is the only runtime dependency. `PyYAML` is the optional
`[refgraph]` extra, used solely to parse Prometheus rule files. The
smaller the surface, the fewer of these paragraphs anyone has to trust.
