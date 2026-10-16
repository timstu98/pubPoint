# Architecture decisions

An ADR records one significant choice that may govern multiple designs or be reconsidered independently of its original project. Include the context, meaningful alternatives, decision, and consequences. Keep implementation details in [technical designs](../development/designs/README.md), and link between the two without repeating the analysis.

Mark each ADR as proposed, accepted, or superseded. Preserve an accepted record as history; document a changed choice in a new ADR that links back to it. Small choices specific to one piece of work belong in its design.

The initial stack choices are recorded below. Database hosting is a separate decision from the database engine.

- [001: Use React for the frontend](001-react-frontend.md)
- [002: Use Flask for the backend](002-flask-backend.md)
- [003: Use MySQL as the relational database](003-mysql-database.md)
