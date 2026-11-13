# Hosted API prototype

This folder is an **undeployed prototype**. It sketches a hosted API:
Starter, Pro and Unlimited tiers, metering, async jobs, and an OpenAPI
description. None of that is running anywhere. It takes no money. Auth
is a stub that hands every caller a development account, there is no
persistence, and `InMemoryJobStore` breaks behind more than one worker.
All three refuse or warn rather than failing quietly. Do not deploy it,
and do not put a price on it.

The tools that exist are the local CLI (`pip install redd-munro`,
command `redd`) and the in-browser auditor at
[reddmunro.com](https://reddmunro.com). Both stay free under
Apache-2.0. Both run on the machine of the person using them. Nothing
in this folder changes that, and nothing here is a product you can buy.

```bash
pip install "redd-munro[server]"    # fastapi, uvicorn — optional
python test_backend.py              # service and jobs, no HTTP
python test_schemas.py              # the models match a real audit
```
