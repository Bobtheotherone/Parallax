# Scope

**Owner:** human/operator  
**Current revision:** `SCOPE-REV-0001`  
**Status:** TEMPLATE — populate from the governing competition rules before any live run.

This file states the exact authorized boundary. It is read by Daybreak and the Scope Executor; Forge normally does not need it.

## Competition / environment

- Competition:
- Environment:
- Start time:
- End time:
- Rules source:
- Human operator:

## Allowed destinations

| Destination ID | Host / environment | Allowed operation classes | Notes |
|---|---|---|---|
| `DEST-...` |  |  |  |

## Controlled principals

| Principal ID | Description | Allowed roles |
|---|---|---|
| `PRINCIPAL-...` |  |  |

## Request budgets

- global request budget:
- per-destination budget:
- max request rate:
- max concurrency:
- retry policy:
- time-window constraints:

## Hard prohibitions

Populate directly from rules. Typical classes to encode mechanically include:

- unrelated third parties;
- out-of-scope hosts/accounts;
- destructive or irreversible mutation unless explicitly permitted;
- persistence beyond competition needs;
- credential theft or secret collection;
- denial-of-service/stress behavior;
- uncontrolled enumeration;
- actions that bypass a required human-only step.

## Human-only actions

Examples may include flag submission, scope expansion, destructive cleanup outside pre-authorized campaign-created artifacts, or rules-ambiguous operations.

## Executor decision model

Every proposed live action must resolve to one of:

`ALLOW | DENY | REQUIRE_HUMAN | BUDGET_EXHAUSTED | RATE_DEFER | INVALID_REQUEST`

No target-side transmission occurs before `ALLOW`.

## Amendments

Append scope changes here with:

- new revision ID;
- date/time;
- authorizing human;
- exact rule change;
- affected destinations/principals/budgets;
- runs invalidated or newly enabled.

Never silently edit history.
