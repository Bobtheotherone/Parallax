# Source-Pack and Handoff Ingestion

Large knowledge folders, handoff ZIPs, raw-source corpora, trace bundles, literature packs, and external-model returns are **source packs**. Their layouts may change over the project lifetime.

## Principle

Do not hard-code the control plane to a current ZIP structure. Register each pack, preserve provenance, and project only validated facts into the world model.

## Ingestion protocol

1. **Register**
   - allocate `PACK-NNNN`;
   - record filename/display name;
   - record acquisition date and origin;
   - record byte size and cryptographic digest when available.

2. **Classify**
   - raw source;
   - runtime receipts;
   - external research;
   - prior handoff;
   - generated materialized view;
   - historical strategy;
   - benchmark/eval pack.

3. **Sanitize**
   - reject raw secrets from Markdown;
   - retain typed redactions and hashes;
   - preserve an omission ledger for intentionally excluded artifacts.

4. **Index**
   - record stable internal artifact references;
   - preserve source URI → pack path mappings when useful;
   - do not rely on absolute machine-local paths.

5. **Validate**
   - distinguish exact source, runtime observation, inference, and inherited conclusion;
   - validate schemas if supplied;
   - identify stale or generated views.

6. **Project**
   - add only evidence-supported facts to `WORLD.md`;
   - add uncertainties to `HYPOTHESES.md`;
   - add contradictions to `EVIDENCE.md`;
   - add generic capability gaps to `FORGE_QUEUE.md`.

7. **Freeze**
   - never mutate the original source-pack digest after registration;
   - if corrected, register a new pack and link supersession.

## Handoff rule

A prior handoff may contain useful synthesis, but it is not automatically campaign truth. Prefer independently reconstructable evidence.

## Generated-view rule

Materialized views such as “current world,” “active frontier,” or search indexes are caches. Their backing receipts outrank them when the two disagree.

## Retrieval rule

Default retrieval should favor:

1. current scope;
2. current world;
3. current strategy epoch;
4. evidence receipts;
5. capability registry;
6. source indexes;
7. archived strategy only when explicitly requested.
