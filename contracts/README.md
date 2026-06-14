# Contracts

Machine-readable interface specs — the formal, testable surface of the system. Two
kinds live here:

- **Internal service contracts** — the HTTP / event boundaries *between* services
  (TypeSpec → OpenAPI, plus AsyncAPI for messaging). Service pages embed these, and
  they're what `oasdiff` / `schemathesis` / `prism` verify.
- **Public / external API specs** — the OpenAPI / AsyncAPI for APIs and webhooks
  exposed to customers and partners. These feed the public-facing docs under
  `docs/interfaces/` (when that area exists) as well as verification.

This directory holds the **specs**; the human-readable docs that explain them live
under `docs/` (service pages for internal contracts; `docs/interfaces/` for public
APIs/webhooks/SDKs).

## Layout — one project per service or API

```
contracts/
  <service-or-api>/
    package.json      # pins @typespec/* (a TypeSpec contract is a project)
    tspconfig.yaml    # emitter config
    main.tsp          # the source
    openapi.yaml      # compiled output (committed; regenerate from main.tsp)
    asyncapi.yaml     # event contract, if the service emits/consumes events
```

Start one by copying **`templates/contract/`** to `contracts/<name>/`.

## Authoring (TypeSpec → OpenAPI)

A TypeSpec contract resolves its libraries from a local `node_modules`, so each
project installs its own deps. Run inside the toolkit (`make shell` at the repo
root):

```bash
cd contracts/<name>
npm install            # once
tsp compile main.tsp   # -> _out/openapi.yaml ; copy to openapi.yaml when stable
```

(`node_modules/` and `_out/` are gitignored; commit `main.tsp` + the generated
`openapi.yaml`.)

## Verification

- **Backward-compat** (offline): `oasdiff breaking old.yaml new.yaml --fail-on ERR`
  (HTTP) · `asyncapi diff old.yaml new.yaml` (events).
- **Provider conformance** (needs the running service): `schemathesis run
  openapi.yaml --base-url <host>`.
- **Mock / validating proxy**: `prism mock openapi.yaml` · `prism proxy openapi.yaml
  <host>`.

See `TOOLKIT.md` for the live-stack caveats, and `example/contracts/` for a worked
example.
