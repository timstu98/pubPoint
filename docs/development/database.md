# Database Document

> **Living reference**
>
> Update this page when the implemented data model changes.

## Implementation

The application uses MySQL 8.0 with Flask-SQLAlchemy.

## Schema

The current model includes users, groups, pubs, user-group queries, locations, distances, and Bayesian-model training data.

The model definitions remain authoritative for columns, relationships, indexes, and constraints. Migration configuration remains authoritative for schema migrations.

## Open questions

- Is a migration thing necessary at this stage? Is it a good learning?
- Likely worth outlining the key schemas (the schemas for the key objects of our database) and accepting these will change after we scope a full set of designs.
