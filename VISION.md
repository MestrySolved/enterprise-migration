# Vision

## The problem

Cloud migration assessment work — figuring out what an organization's
applications depend on, deciding a migration strategy for each one (the 7Rs:
Rehost, Replatform, Refactor, Repurchase, Retire, Retain, Relocate), sizing
the target infrastructure, and flagging security/compliance needs — is
repeatable, structured work that currently gets redone manually, from
scratch, for every engagement. It's exactly the kind of documentation and
solution-design work that eats time under deadline pressure (e.g. in a
presales scoping exercise) despite following the same underlying logic each
time.

## What this tool does

**Input:** a description of an organization's applications/systems — either
typed in interactively (dynamic input) or provided as a structured file
(static input) — including each system's dependencies, criticality,
operating system, resource needs (CPU/memory/storage), internet exposure,
compliance requirements, and workload type.

**Process:** the tool builds a dependency graph, applies rule-based 7R
migration logic, layers a local AI model's critique on top of that
recommendation, determines an appropriate hosting model (VM / Kubernetes /
SaaS) and machine size, flags security and compliance considerations, and
maps each recommendation to the specific GCP migration tool and pricing
calculator needed next.

**Output:** a complete, per-system migration plan — not just a
classification, but the practical next steps and tools someone would
actually need to price and execute the migration.

## Why it's built this way

- **Rule-based logic first, AI second** — the rules give a transparent,
  explainable baseline; the AI model's job is to critique and refine that
  baseline, not replace it. This keeps the reasoning auditable rather than
  being a black box.
- **Local AI (Ollama), not a paid API** — removes cost as a barrier to
  building and demonstrating this, and keeps data fully on-device, which
  matters for any real inventory data that shouldn't leave a company's
  network.
- **GCP-only, on purpose** — going deep on one provider's actual tools and
  pricing model produces a more useful, concrete output than a shallow
  multi-cloud abstraction would at this stage.

## What this is not (yet)

This is a working prototype built to demonstrate the concept and the
underlying thinking — not a production-grade or enterprise-scale tool. It
does not currently:

- Scan live cloud environments automatically (input is manual/interactive)
- Support multiple cloud providers
- Pull real-time pricing data
- Provide a graphical interface

## Where it could go next

- **Live discovery** — connect to GCP's Asset Inventory or similar APIs to
  build the dependency graph automatically instead of requiring manual input
- **Multi-cloud** — extend the tool-mapping layer to AWS and Azure
  equivalents
- **Confidence scoring** — have the AI layer flag how confident it is in a
  recommendation, and surface disagreements between the rule-based and AI
  layers explicitly rather than just printing both
- **A real interface** — a simple web UI instead of CLI output, so the tool
  could be used in a live client conversation rather than a terminal

This document is meant to stay a short, honest description of what the
project actually does today — it should be updated as the tool grows, not
left as an aspirational wishlist that drifts from reality.
