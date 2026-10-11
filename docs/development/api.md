# API Document

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

## REST API

Represetational State Transfer → Despite having principles seen as more lightweight and scalable than other more prescribed protocols like SOAP.

CRUD → basic creation, read, update and delete of data storage

This has been recommended as a great guide: https://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api

### Major principles

- Uniform Interface
- Client-server
- Stateless
- Cacheable
- Layered System
- Code on demand (Optional)

### OpenAPI

OpenAPI (formerly Swagger) is a standard for describing RESTful APIs in a machine-readable format, such as YAML or JSON. It defines endpoints, request and response formats, and authentication methods, making APIs easier to document, test, and integrate. Tools built around OpenAPI can generate documentation, client libraries, and server stubs, saving time and improving reliability, especially in collaborative or complex projects.

For a small personal project with one or two developers, OpenAPI may not be necessary. The added effort to maintain the specification might not justify its benefits when the API is simple, and the developers are familiar with the codebase. Clear code organization and documentation are often enough. If the project grows in complexity or requires external collaboration, OpenAPI can be introduced later as needed.

### Http Methods

- Only use following, doest necessarily always have to follow the same format BUT it MUST be a uniform interface:
  - GET - Return the resource or a collection of resources.
  - PUT - Full Update. Replace a specific reource or collection of resources using an id. If an id is known before hand, it can be used to create a resource.
  - PATCH - Partial Update. Update a specific resource or a collection of resources by an id. No body.
  - POST - Creates a new resource. Can be used for operations that don’t fit into other categories.
  - DELETE - Remove a specific resource by an id. No body whatsoever.

Note, the ability to use Post as a general method for operations that do not easily fit into another method.

Consistency is the hardest thing to get right and the most important thing for your user. Work hard at this.

### URL Hierarchy

This is the art part of making a great API.

Use ids in the URL rather than query-string, ie. dont have the id in the “…?id=123” but instead “user/123”. Instead, use query-string parameters for filtering, but not for resource names.

Use the hierarchal nature of the URL to imply structure.

Design for the user/client.
