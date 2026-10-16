# MVP technical design and implementation order

> **Draft**
>
> Major technical slices for the [MVP](../../product/mvp-prd.md), in implementation order. Each slice will have its own focused design.

## Approach

Build on the current [React, Flask, and database architecture](../architecture.md).

Refine the living data model and frontend guidance as each slice is designed and implemented. Use migrations for schema changes.

Develop and test locally using Docker Compose for the frontend, backend, and database. Run automated tests and manual journey checks locally, with no staging builds or deployments initially. This keeps feedback quick and avoids cloud infrastructure costs during development.

Keep the frontend rough and ready, with working validation, loading, and error states. Visual polish is the final development task, after the core journeys work together.

## Implementation sequence

| Order | Slice                                        | Technical scope                                                                                                                                                                                                                                                                                                                                |
| ----- | -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0     | **Initial living documentation**              | Sketch entities, relationships, ownership, and known constraints in the [database reference](../database.md). Define screens and navigation in `docs/development/frontend.md`. Update [architecture](../architecture.md) and [API](../api.md) guidance where needed. Review the drafts against MVP journeys before feature work. |
| 1     | **Data foundations and London venues**       | Decide MySQL versus PostgreSQL/PostGIS before expanding the spatial schema. Validate the [population design](pub-database-population.md): venue coordinates, repeatable imports, coverage, deduplication, and API usage. Then carry out this hydration.                                                                                        |
| 2     | **Algorithm baseline**                       | Implement and evaluate the [MVP algorithm baseline](../../search-algorithm/mvp.md), with code under [backend algorithms](../../../app/backend/algorithms/). |
| 3     | **First ad hoc venue search**                 | Connect the baseline to a basic search interface and API. Accept participants, starting points, and one transport type each. Define the search contract, participant state, validation, and failure handling. Use local fixtures before accounts exist. |
| 4     | **Accounts, sign-in, and personal defaults** | Choose an authentication method and define sessions, onboarding, and recovery. Save and validate a home address and default transport type. Protect account settings and connect defaults to search preparation.                                                                                                                               |
| 5     | **Search preparation and comparison**        | Add address/venue entry, geocoding, map adjustments, home/work/custom/current location choices, participant and transport changes, repeat searches, and external directions. Define location consent, search state, and retry behavior. Keep search inputs separate from saved defaults.                                                 |
| 6     | **Reusable groups and membership**           | Create and manage groups, accepted memberships, and permissions. Start searches from group members and their defaults. Implement the PRD's address-sharing rule. Search edits must not silently update saved groups or personal defaults.                                                                                                      |
| 7     | **Guests and invitations**                   | Support guests without accounts and invitations by email or phone. Define recipient verification, delivery, expiry, acceptance, and decline. Acceptance grants membership and links any guest entry to the account, preserving search inputs and granting originating-search access. Pending invitations grant no saved-group access.          |
| 8     | **Shared searches**                          | Define who can edit, how updates reach other members, and how parallel searches and conflicting edits behave. Give authorised members access to shared inputs and results. Collaboration and confirmation rules remain open in the PRD.                                                                                                        |
| 9     | **Deployment and validation**                | Once core journeys work locally, follow the [deployment design](mvp-deployment.md) for private staging on ECS/Fargate and RDS, with separate configuration and test data. Cover secrets, access, migrations, health checks, logs, cost controls, and rollback. Validate integrated journeys before production release.                         |
| 10    | **Final frontend polish**                    | Refine layout, wording, accessibility, and mobile/desktop behavior after staging validation. Recheck critical journeys. Production rollout follows validation and polish.                                                                                                                                                                      |

## Verification

Use unit tests for individual logic, integration tests for API/database interactions, and end-to-end tests for the main user journeys. Check permissions and address visibility across accounts, groups, and invitations.

Add golden tests for the algorithm: fixed participant inputs, venue data, and routing responses with reviewed expected recommendations and rankings. Review changes to those expectations when the algorithm changes. Measure real API usage, latency, and recommendation quality separately. Keep detailed algorithm test scenarios in the [algorithm plan](../../search-algorithm/mvp.md#testing-and-evaluation).

Resolve the [PRD's open questions](../../product/mvp-prd.md#assumptions-and-open-questions) in the relevant designs, including privacy, group permissions, invitation lifetime, and collaboration.
