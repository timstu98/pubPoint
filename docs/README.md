# Project Documentation

This directory is the repository’s durable context for product direction, architectural decisions, implementation guidance, and research. Prefer these documents over external planning notes when working on the project.

Keep each fact or decision canonical in one document. Use links between documents instead of repeating the same guidance in multiple places.

## Where information belongs

| Path | Purpose |
| --- | --- |
| [`product/`](product/) | [Vision](product/vision.md) and [product MVP requirements](product/mvp.md): what users should be able to do, including scope and journeys. |
| [`search-algorithm/`](search-algorithm/) | Venue recommendation research, the cost baseline, and the evolving [algorithm MVP plan](search-algorithm/mvp.md): how we currently intend to suggest venues. |
| [`development/`](development/) | General engineering guidance: [workflow](development/ai-workflow.md), architecture, API, and database. |
| [`development/research/`](development/research/) | Supporting investigations into [provider costs](development/research/api-cost-research.md) and [pub database population](development/research/pub-database-population.md). |
| [`decisions/`](decisions/) | Durable choices and their reasoning, such as the pub database population strategy. |
| [`images/`](images/) | Assets used by the documentation. |
