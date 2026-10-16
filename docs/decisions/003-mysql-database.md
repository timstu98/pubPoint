# Use MySQL as the relational database

> **Accepted**

PubPoint will store users, groups, memberships, pubs, and searches. A user can belong to several groups, and each search will refer to its participants and candidate venues. A relational database lets me store each fact once, connect records through keys, and reject links to users or pubs that do not exist. Transactions can keep related changes together, such as creating a group and its first membership. I will use MySQL for this model; it meets these needs and I know it slightly better than PostgreSQL.

PostgreSQL would also handle this model. I do not have an MVP requirement that clearly favors either engine, so familiarity is a tie-breaker rather than a technical advantage. A document database would offer a more flexible schema, but it would make these relationships and their constraints less direct. Choosing MySQL does not decide where it runs: standard RDS for MySQL and Aurora MySQL-Compatible are separate hosting options to weigh when planning deployment.
