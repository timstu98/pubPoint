# Technical designs

Keep one design here for each substantial feature or technical change. A design explains how the change could be implemented and is reviewed before work starts. Scope it around a capability, such as group membership or venue search, rather than splitting a single user journey into frontend, backend, and database documents. Include all affected layers in the same design when useful.

Each design should state its status (draft, in review, accepted, or superseded), link to relevant [MVP PRD](../../product/mvp-prd.md) requirements when applicable, and cover the proposed approach, meaningful alternatives, affected interfaces and data, risks, and how the result will be verified. Name files by capability, for example `group-membership.md`. Small changes can be covered by the issue or PR without a separate design.

Designs record a proposed or agreed approach and the choices specific to that work. In this repo, RFC means a design circulated for comments: it is the review stage, not a separate document type. Once accepted, it remains a design, though people may still call it an RFC informally. Record a choice that will govern later designs or can change independently in an [ADR](../../decisions/README.md); link to it here instead of repeating its analysis. Keep supporting measurements and experiments in [research](../research/) and link to them. Once a change is built, update the living architecture, API, or database reference where needed; those references describe the current system.

The [MVP algorithm plan](../../search-algorithm/mvp.md) is an existing focused design kept with the algorithm research. New general feature designs belong here.
