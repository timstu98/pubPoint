# Project Documentation

This directory is the repository’s durable context for product direction, architectural decisions, implementation guidance, and research. Prefer these documents over external planning notes when working on the project.

Keep each fact or decision canonical in one document. Use links between documents instead of repeating the same guidance in multiple places.

Product, design, and decision documents define the work. Create GitHub issues from those documents to track implementation, and link issues back to the relevant documents. Keep issue numbers and task status in the issues rather than the durable documents.

For plain-language definitions of common B2C product and engineering documents, see [Common product and engineering documents](document-types.md).

The [PubPoint glossary](../GLOSSARY.md) defines the product's core terms.

## How PubPoint's documents fit

- **Vision and strategy:** [Product vision](product/vision.md) describes the problem, audience, and recommendation goals. There is no committed roadmap yet.
- **Business case:** [Business case](product/business-case.md). Its figures and ideas are working assumptions.
- **Future ideas:** [Product ideas](product/ideas.md) captures possibilities beyond the current MVP.
- **PRD:** The [MVP PRD](product/mvp-prd.md) covers overall outcomes, scope, user journeys, shared requirements, and open questions. It is still proposed, and some quality targets remain to be defined.
- **Technical designs:** Plans for substantial technical changes belong in [development/designs/](development/designs/). The [MVP technical design overview](development/designs/mvp-technical-design.md) orders the major implementation slices. We call a design an RFC while requesting comments on it; once accepted, it remains an accepted design. Choices specific to that work stay in the design.
- **ADRs:** [Decision records](decisions/) preserve significant choices that may guide later designs or be reconsidered independently. Designs link to relevant ADRs instead of repeating their analysis.
- **Living references:** [Architecture](development/architecture.md), [API](development/api.md), [database](development/database.md), and [frontend](development/frontend.md). Keep draft model and screen guidance clearly marked alongside current implementation. Code and migrations define the exact implemented behavior and schema.

The MVP PRD covers the product as a whole, so several designs may address different parts of it. There is no expected one-to-one mapping: each design should link to the requirements it addresses.

The vision and MVP currently express hypotheses and intended outcomes. User study findings and measured results can be documented when available.

## Where information belongs

| Path                                             | Purpose                                                                                                                                                                                                                              |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`product/`](product/)                           | [Vision](product/vision.md), the [MVP PRD](product/mvp-prd.md), and the [business case](product/business-case.md).                                                                                                                   |
| [`search-algorithm/`](search-algorithm/)         | Venue recommendation research, the cost baseline, and the evolving [algorithm MVP plan](search-algorithm/mvp.md): how we currently intend to suggest venues.                                                                         |
| [`development/`](development/)                   | [AI workflow](development/ai-workflow.md) and living architecture, API, database, and frontend references.                                                                                                                                     |
| [`development/designs/`](development/designs/)   | Proposed and accepted plans for substantial technical changes.                                                                                                                                                                      |
| [`development/research/`](development/research/) | Supporting investigations and evidence for designs and living references.                                                                                                                                                           |
| [`decisions/`](decisions/)                         | Lasting technical choices, their alternatives, and consequences.                                                                                                                                                                    |
| [`images/`](images/)                             | Assets used by the documentation.                                                                                                                                                                                                    |
