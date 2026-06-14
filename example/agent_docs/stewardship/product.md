# Product: Beacon

> **Fictional reference product** — demonstrates a completed bootstrap. None of
> this is real.

## What it is

Beacon is a customer-messaging SaaS. Organizations subscribe to a plan, then send
their customers transactional and campaign messages. Billing, account management,
and message delivery are handled by separate backend services behind one web app.

## Domains

- **Accounts** — organizations, users, seats. (`accounts-service`)
- **Billing** — plans, subscriptions, invoices, proration. (`billing-service`)
- **Messaging** — templates, scheduling, delivery, delivery logging. (`messaging-service`)

## Repositories

| Repo | Language / stack | Role |
|------|------------------|------|
| `beacon-accounts` | Java / Spring, MySQL | orgs & users |
| `beacon-billing` | Ruby / Rails, MySQL | plans, subscriptions, invoices |
| `beacon-messaging` | Elixir / Phoenix, PostgreSQL + MongoDB + RabbitMQ | sending + delivery log |
| `beacon-web` | TypeScript / React | the web UI |

## Documentation scope

- In scope: features, services (as black boxes + contracts), data/domain models,
  and decisions across the four repos above.
- Non-goals (for now): deployment/infra runbooks, third-party provider internals,
  and any modification of the source code. Named here so a cold reader sees the
  decline; revisit deliberately, not by drift.
