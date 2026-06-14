# Contracts (example)

Demonstrates the contract pipeline end to end on a toy spec, so the toolchain is
proven before it touches the real system.

```
contracts/
├── billing/
│   ├── main.tsp        # TypeSpec source (authoring layer)
│   └── openapi.yaml    # compiled output (what the tools consume)
└── messaging/
    └── asyncapi.yaml   # RabbitMQ events (AsyncAPI)
```

## Authoring: TypeSpec → OpenAPI

Author HTTP contracts in **TypeSpec** and compile to OpenAPI. The compiled
`openapi.yaml` is the artifact every downstream tool reads (and what gets embedded
into the [billing-service](../docs/services/billing-service.md) page).

A TypeSpec contract is a small **project** — it resolves its libraries from a local
`node_modules` (unlike the file-based tools below). `billing/` is set up that way:
`package.json` pins the deps and `tspconfig.yaml` configures the emitter.

```bash
cd billing
npm install            # one-time: fetch the pinned @typespec/* libraries
tsp compile main.tsp   # -> _out/openapi.yaml ; copy to openapi.yaml when stable
```

Run these from a toolkit shell (`make shell` at the repo root) so node / tsp /
oasdiff / schemathesis / prism are all on PATH.

## Verification trio

Chosen over a single platform (e.g. Specmatic) for being lighter and OpenAPI-centric.
Each tool covers a different point in the lifecycle:

### 1. Backward compatibility — oasdiff (Go)

Gate breaking changes in CI by diffing the new spec against the last released one.

```bash
oasdiff breaking billing/openapi.baseline.yaml billing/openapi.yaml --fail-on ERR
```

### 2. Provider conformance — Schemathesis (Python)

Does the **running** service actually match its spec? This is our primary
reverse-engineering check: write the inferred spec, then let Schemathesis fuzz the
real service against it and report every divergence.

```bash
schemathesis run billing/openapi.yaml --base-url http://localhost:4000 --checks all
```

### 3. Validating proxy / mock — Prism (Node)

Mock the service from the spec, or proxy live traffic and flag responses that
violate it.

```bash
prism mock billing/openapi.yaml                      # mock server
prism proxy billing/openapi.yaml http://localhost:4000   # validate live traffic
```

## Async note

oasdiff is **OpenAPI-only**. For AsyncAPI (`messaging/asyncapi.yaml`) backward-compat,
use the AsyncAPI CLI:

```bash
asyncapi diff messaging/asyncapi.baseline.yaml messaging/asyncapi.yaml
```
