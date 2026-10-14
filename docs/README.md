# Project Documentation

This directory is the repository’s durable context for product direction, architectural decisions, implementation guidance, and research. Prefer these documents over external planning notes when working on the project.

Keep each fact or decision canonical in one document. Use links between documents instead of repeating the same guidance in multiple places.

For plain-language definitions of common B2C product and engineering documents, see [Common product and engineering documents](document-types.md).

## How PubPoint's documents fit

- **Vision and strategy:** [Product vision](product/vision.md) describes the problem, audience, and recommendation goals. There is no committed roadmap yet.
- **Business case:** [Business case](product/business-case.md). Its figures and ideas are working assumptions.
- **PRD:** The [MVP PRD](product/mvp-prd.md) covers overall outcomes, scope, user journeys, shared requirements, and open questions. It is still proposed, and some quality targets remain to be defined.
- **Technical designs / RFCs:** New proposals for substantial features belong in [development/designs/](development/designs/). Each design can cover frontend, backend, and database together. The existing [algorithm MVP plan](search-algorithm/mvp.md) stays with its [research](search-algorithm/research.md).
- **ADR:** [Decision records](decisions/) capture durable choices.
- **Current system reference:** [Architecture](development/architecture.md), [API](development/api.md), and [database](development/database.md) are separate living references for their subjects. Code and migrations define the exact implemented behavior and schema.

The MVP PRD covers the product as a whole, so several designs may address different parts of it. There is no expected one-to-one mapping: each design should link to the requirements it addresses.

The vision and MVP currently express hypotheses and intended outcomes. User study findings and measured results can be documented when available.

## Where information belongs

| Path                                             | Purpose                                                                                                                                                                                                                              |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`product/`](product/)                           | [Vision](product/vision.md), the [MVP PRD](product/mvp-prd.md), and the [business case](product/business-case.md).                                                                                                                   |
| [`search-algorithm/`](search-algorithm/)         | Venue recommendation research, the cost baseline, and the evolving [algorithm MVP plan](search-algorithm/mvp.md): how we currently intend to suggest venues.                                                                         |
| [`development/`](development/)                   | [AI workflow](development/ai-workflow.md) and living architecture, API, and database references.                                                                                                                                     |
| [`development/designs/`](development/designs/)   | Technical designs and RFCs for substantial features, with one document per capability where useful.                                                                                                                                  |
| [`development/research/`](development/research/) | Supporting investigations into [API conventions](development/research/api-research.md), [provider costs](development/research/api-cost-research.md), and [pub database population](development/research/pub-database-population.md). |
| [`decisions/`](decisions/)                       | Durable choices and their reasoning, such as the pub database population strategy.                                                                                                                                                   |
| [`images/`](images/)                             | Assets used by the documentation.                                                                                                                                                                                                    |
