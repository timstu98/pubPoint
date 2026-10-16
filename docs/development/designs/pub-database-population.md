# Pub database population

> **Accepted approach; implementation still needs validation**

## Goal

Collect a useful set of London pubs and bars for the [MVP venue search](../../product/mvp-prd.md#find-a-venue-for-a-meetup). One broad Places search returned a limited, central set in the [population research](../research/pub-database-population.md). Keep API usage measurable before running the job regularly.

## Approach

Use Google Places Text Search over a grid of rectangular areas. Restrict each search to its rectangle, follow any page tokens, combine the results, and remove duplicates before storing candidates. The [current utility](../../../app/backend/api/utils/populate_pubs.py) defines the London bounds and divides them into 8 rows and 12 columns.

![Approximate London pub search area](../../images/populate_pubs_size.png)

The grid spreads requests across London and provides a simple baseline for measuring coverage and cost. It cannot guarantee complete coverage: a cell may still hit an API result limit, and denser areas may need smaller cells. The [research note](../research/pub-database-population.md) holds the API findings, coordinate experiments, and measurements to collect.

## Alternatives

- **One London-wide search:** Fewer requests, but the observed results covered only a small part of the city.
- **Concentric, elliptical, or adaptive search areas:** Could give central London more attention, but add complexity before the grid's gaps have been measured.
- **Nearby Search:** Its result limits made it a weaker fit for this collection job; see the research note for the API comparison.

## Before regular use

Compare the search terms `pub` and `bar`; the current utility sends `bar`. Measure result quality and billed requests, including pagination, before choosing a term or refining the grid. The current utility also skips database inserts unless `TEST_FUNCTIONALITY_MODE` is true, so its write behavior needs confirmation before a population run is scheduled.
