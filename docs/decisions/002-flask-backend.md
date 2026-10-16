# Use Flask for the backend

> **Accepted**

PubPoint needs an HTTP API for accounts, groups, venues, and recommendations. I want to write the recommendation logic in Python, so I will use Python for the API as well and build it with Flask. Flask provides routing and request handling without imposing a larger application structure, which suits the MVP's modest API.

Django would provide more built-in features, such as an admin and authentication patterns, but I do not yet need that full framework. A Node backend would share a language with the frontend, but the recommendation code would then need to move to JavaScript or run separately. Flask leaves more choices, such as persistence and authentication, for us to make explicitly. I accept that tradeoff for a small Python API.
