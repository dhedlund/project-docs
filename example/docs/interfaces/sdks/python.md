---
title: Python SDK
type: sdk
status: active
reviewed_confidence: 65
last_reviewed: 2026-06-14
sources:
  - repo: beacon-sdks
    branch: main
    sha: e5f6a7b
    committed: 2026-05-25
    paths:
      - python/
domain: messaging
tags: [sdk]
---

# Python SDK

> The official Python client for the [Messaging API](../api/index.md).

## Install & authenticate

```python
# pip install beacon
from beacon import Beacon
client = Beacon(api_key="sk_live_...")
```

## Quickstart

```python
msg = client.messages.send(to="user@example.com", channel="email", template="welcome")
print(msg.id, msg.status)
```

## Version compatibility

| SDK version | API version | Notes |
|-------------|-------------|-------|
| 2.x | 2026-05-01+ | current |
| 1.x | 2025-08-01 | security fixes only |

## Notes & nuances

??? info "Generated vs hand-written"
    Model classes are codegen'd from the OpenAPI spec; the ergonomic helpers
    (retries, pagination) are hand-written.
