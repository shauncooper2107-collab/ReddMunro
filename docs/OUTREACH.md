# Cohort outreach — the note, the reply shape, the record

Operational companion to `ADOPTION_PREREG.md`. The protocol there is
fixed; this file is how it actually gets asked.

**The one rule: the note must not mention the predictions.** A1 says
teams stall getting an export into shape. Telling someone that before
asking where they stopped is not a question, it is a suggestion, and the
answer stops being evidence. Nothing below names a prediction, a
suspected friction point, or a hoped-for finding.

---

## 1 · The note

Short on purpose. The recipient is being asked for twenty minutes and a
reply, by a stranger, about a tool they did not ask for.

> **Subject:** two panels on our Prometheus box were the same series
>
> Hi [name] —
>
> Quick one. I built an open-source tool that reads a dashboard export
> and works out how much of the board is measuring the same thing —
> which panels restate each other, and which are candidates to archive.
>
> On the public Prometheus corpus it ships with, **11 metrics carried
> 5.6 independent signals**: half the board was a restatement of the
> other half. Two of the archive candidates turned out to sit behind
> live alert rules, which is the part I actually care about — the
> arithmetic says drop it, the alert says do not.
>
> **Nobody has run it on a dashboard they would be paged for.** I am
> looking for ten teams to do that. Nothing to buy, no call, no trial.
> Apache 2.0, runs locally, nothing is uploaded — there is no network
> code in it and a test that asserts so.
>
> **Two minutes, nothing installed:** open reddmunro.com and click
> *Try the example dashboard*. That is the whole engine running in your
> tab.
>
> **Twenty minutes, on your own board:**
>
> ```
> pip install redd-munro
> redd run your_export.csv
> ```
>
> Getting the export is the fiddly part, so it is written up here:
> github.com/bigangusmac67-oss/ReddMunro#getting-the-csv — in Grafana it
> is Panel → Query Inspector → Data → Join by time → Download CSV.
>
> Works best if your alert rules and dashboards are in git: point it at
> them with `--refs` and it flags any archive candidate something still
> depends on. That part reads Prometheus rule YAML and Grafana JSON
> only — on Datadog or New Relic you get the redundancy audit but not
> the cross-check.
>
> If you try it, three questions — a one-line answer to each is
> genuinely enough:
>
> 1. **What happened when you ran it?**
> 2. **Where did you stop?**
> 3. **Did you do anything as a result?**
>
> A reply saying it found nothing, or that you gave up before it ran, is
> as useful to me as a good finding — more so, since I have no shortage
> of the good kind on public data. Results get written up including the
> nulls; your team is not named unless you ask to be.
>
> — Shaun
> shaun@reddmunro.com · github.com/bigangusmac67-oss/ReddMunro

### Notes on sending

**Do not use this note on Reddit, HN, or any public forum.** See §1b. It
is written for one named person who can reply privately, and a public
board punishes that register hard.

---

## 1b · The public-forum version (Reddit, HN, Slack communities)

> ### r/sre — DO NOT POST THE DRAFT BELOW
>
> Rules read 24/08/2026. Two of the seven rule it out:
>
> - **Rule 6 — No Advertisements.** A post about a tool you built, with
>   links to it, is an advertisement under a plain reading. Apache 2.0
>   and no price tag does not exempt it; that is a licence, not a
>   category. **Message the mods before posting anything.** The button is
>   on the sidebar. Say what it is, say you wrote it, say it is not
>   commercial, and ask whether it belongs in the subreddit or a weekly
>   thread. If they say no, that is the answer.
> - **Rule 7 — No AI-Generated Posts.** The draft below was drafted with
>   an assistant. Posting it would break the rule whatever it says.
>   **Anything posted to r/sre must be written by Shaun, in his own
>   words, from scratch.**
>
> The draft is kept as a **content checklist** — what a post needs to
> cover and in what order — not as text to paste. The private email in
> §1 is unaffected: it is one person writing to another, and no rule
> governs how someone drafts their own correspondence.

**Before posting anywhere: read the subreddit rules.** Many technical
subreddits ban self-promotion outright or confine it to a weekly thread,
and local rules override Reddit's global 90/10 norm. If the rules are
ambiguous, message the moderators first and say plainly what you want to
post. A removed post costs a day; a domain blacklisted for spam costs the
project.

**This cannot supply the `direct` sample.** Anyone arriving from a public
post has read the post and will click through to the site, where
prediction A1 is published. Everyone from this channel is recorded
`source: site` and is contaminated for A1 by `ADOPTION_PREREG.md`
Amendment 1. **Public forums are for reach; the cold email is for
evidence.** At least five `direct` contacts are still required.

**What changes, and why.** The email leads with the tool because it is
addressed to someone who was chosen. A forum post is read by people who
chose nothing, so it has to lead with the *finding* and earn the rest.
Bold section headers, "nothing to buy, no call, no trial", and a
three-question ask all read as marketing cadence in a thread, however
honest they are. And the limitations move to the top: on a technical
forum, what your tool cannot do buys more credit than any claim about
what it can.

> **Title:** Two panels on a public Prometheus corpus were the same
> series (r = 0.99987) — and one was behind a paging alert
>
> Full disclosure up front: I wrote the tool at the bottom of this post.
> The finding is the interesting part, so it goes first.
>
> Auditing a public Prometheus corpus — 11 metrics, 437 samples — two
> columns matched at r = 0.99987. Not similar, the same numbers on two
> panels, alerting separately. Across the whole board, 11 metrics
> carried about 5.6 independent signals: half of it was a restatement of
> the other half.
>
> The bit I did not expect: the metric with the least unique information
> (0.0011 of its variance was its own) was the one sitting behind a
> `severity: critical` alert. On the arithmetic alone it is the obvious
> thing to delete. Both facts are true and only one of them is in the
> data.
>
> So the tool refuses to say "safe to delete". It emits a worksheet with
> the evidence and four columns only a human can fill — referenced by
> monitors, SLOs, dashboards, runbooks — and cross-checks the first two
> against your Prometheus rules and Grafana JSON if they are in git.
>
> **What it does not do**, since that is usually the useful part:
>
> - does not detect a metric plotted against its own rolling average —
>   two designs built and withdrawn, one produced 476 false positives
> - does not find subset *means*, only exact sums
> - judges integer counters more leniently than gauges, so tied columns
>   are systematically under-flagged
> - nothing in it is causal
> - a metric held flat by a working control loop loses its unique
>   variance and gets offered for archiving — which is exactly the
>   channel that moves when the loop fails. Measured, documented,
>   not fixed
>
> Thirteen of those are written up in the README. Six pre-registrations
> too — predictions committed before pulling each dataset, scored after,
> including the four that failed. One of the failures disproved the
> previous cycle's own diagnosis.
>
> Apache 2.0, numpy only, runs locally, no network code and a test that
> asserts it. `pip install redd-munro`, or drag a CSV onto reddmunro.com
> and it runs in your tab via WebAssembly.
>
> **Nobody has run it on a dashboard they would be paged for.** If you
> do, I would like to know what came back — including "nothing useful",
> which I am short of. Happy to be told the premise is wrong.

**After posting.** Answer questions as an engineer, not as a founder.
When somebody says they ran it, take the three registered questions to
DM in the fixed order — never edited, never as a public reply, because a
threaded answer is performed for an audience and a DM is not.

## 1c · Where outreach is allowed, and where it is not

Checked 24/08/2026. **Read the rules before each channel, not once.**

| Channel | Announce? | Cold DM? | Notes |
|---|---|---|---|
| Cold email, public work address | n/a | **yes** | The only reliable `direct` source. §1. |
| CNCF Slack `#prometheus` | **no** | **no** | See below. |
| r/sre | **no** without mod approval | n/a | Rules 6 and 7. §1b. |
| GitHub Discussions on the repo | yes | n/a | It is our own repo. |
| Catalogue submissions | yes | n/a | `awesome-prometheus`, CNCF landscape — these exist to list tools. |

### CNCF Slack — both doors are closed

The [workspace guidelines](https://www.kubernetes.dev/docs/comms/slack/)
are explicit on two points that matter here:

- **Only official event sponsors may pitch, and only in sponsor
  channels.** A tool announcement in `#prometheus` is not permitted.
  `#prometheus` is a user-support channel; the traffic is people stuck
  on configuration and regressions.
- **Directly messaging users to offer services is not allowed** unless
  they asked. So CNCF Slack **cannot** supply cold `direct` contacts
  either, and the assumption that it could was wrong.

A link posted without context may be deleted. Enforcement runs to a 30-day
ban and a permanent one for repeats.

**What is allowed, and is worth more anyway:** answering questions. The
guidelines actively encourage it — *"there are no stupid questions;
answer simple questions nicely."* Redundant metrics, why everything
correlates during an incident, why differencing changes the answer, why a
total and its parts all look individually redundant: these come up, and
this project now knows the answers cold.

That is a **months-long** route to being someone whose tool people will
try, not a days-long one. Weigh it honestly against the cold email, which
works this week. If somebody's question is genuinely answered by the
tool, naming it inside a real answer is ordinary open-source behaviour —
but the answer has to stand on its own with the link removed, or it is a
pitch wearing a question as a hat.

---

### Facts a post needs, for writing one from scratch

Every figure verified 24/08/2026. Re-derive with `HANDOFF.md` §10.

| Fact | Value |
|---|---|
| Corpus | public Prometheus instance, 11 metrics, 437 samples |
| Headline | 11 metrics carry **5.6** independent signals |
| Redundancy | **49.3%** restates something already on the board |
| The identical pair | `methodGET_status200` ~ `request_rate_total`, **r = 0.99987** |
| Least unique metric | `request_rate_total`, **0.0011** of its variance its own |
| The catch | that metric is behind a `severity: critical` alert |
| Archive candidates | 2 · both flagged CONFLICT by the reference scan |
| Evidence grade | A |
| Engine boundaries | 13 in the README, 7 summarised on the site |
| Pre-registrations | 8 total — 6 scored, 4 of those with published misses |
| Best miss | `BINNING` B3 disproved the previous cycle's own diagnosis |
| Withdrawn detectors | 2 rolling-average designs; one produced 476 false positives |
| Licence / deps | Apache 2.0 · numpy only · no network code, asserted at runtime |

**Ordering that works on a technical forum**, learned from what the
email got wrong: finding first, disclosure in the first line,
limitations in the middle, tool last, and the ask smallest of all. The
worst version leads with "I built a tool"; the best leads with a number
that makes someone check their own board.

---

- **One send, no chase.** The stopping rule counts teams *contacted*;
  a follow-up nudge changes the response rate and therefore the
  denominator. If it becomes necessary, record it as a protocol change
  and score the nudged group separately.
- **Never edit the three questions per recipient.** Tailoring the
  wording to what you suspect that team will say is exactly how a
  registered protocol becomes a leading one.
- **Record the send** in the sheet below on the day it goes out, before
  any reply. A denominator assembled afterwards from replies is not a
  denominator.

---

## 2 · The reply shape

Offered, never required — a form that must be filled is a form that does
not get filled. Freeform replies are scored the same way by hand.

> Copy this in if it is easier than writing prose:
>
> ```
> 1. What happened when you ran it?
>
> 2. Where did you stop?
>
> 3. Did you do anything as a result?
>
> —— optional, factual ——
> board size (panels/metrics):
> audit ran:              yes / no
> produced a worksheet:   yes / no
> worksheet rows filled in:
> ```

The three open questions come first and the factual block second,
deliberately. The factual questions name specific artefacts — worksheet,
rows — and asking them first would tell the respondent which parts of
the process are supposed to matter, contaminating question 2 with the
answer.

**Do not add checkboxes to question 2.** A list like "☐ could not
export ☐ worksheet too long" hands over the very answer being measured.

---

## 3 · The record

One row per team **contacted**, filled on the day of sending. Silence is
an outcome with a row, not a missing row.

| Team | Contacted | Source | Replied | Audit ran | Worksheet | Rows filled | Action taken | Notes |
|---|---|---|---|---|---|---|---|---|

- **Source** — `site` if they came via reddmunro.com, `direct` if
  contacted cold. This column exists because of the contamination
  recorded in `ADOPTION_PREREG.md` Amendment 1: the cohort section of
  the site publishes prediction A1, so anyone arriving that way has
  already been told where we expect them to stop. Their answer to
  question 2 is primed; a `direct` contact's is not. **Score the two
  groups separately or A1 is not measurable.**
- **Replied** — `no` is data. It is the outcome A1 and A2 both predict
  most often, and the one that disappears if only replies are recorded.
- **Rows filled** — a count, not "some". A2 discriminates on whether it
  is zero.

**Scored at ten contacted or 90 days, whichever is first** — including
the case where three replied and seven did not. A response rate that low
would itself be the finding, and it would say more about the ask than
about the worksheet.
