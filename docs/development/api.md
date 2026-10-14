# API Document

> **Living reference**
>
> Update this page when the implemented API changes.

## Implementation

The backend is a Flask application. Routes are registered under `/api/{API_VERSION}`.

Current route modules cover:

- authentication
- groups
- pubs
- users
- user-group queries

## API Testing

I have set up manual tests using postman for all basic CRUD endpoints.

## Background research

The REST API notes and conventions considered for this project are in [API research](research/api-research.md).
