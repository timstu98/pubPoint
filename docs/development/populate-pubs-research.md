# London Pub Population Research

This note records the research and working assumptions behind the pub population utility. The durable implementation decision is recorded in [`docs/decisions/001-populate-pubs-search.md`](../decisions/001-populate-pubs-search.md).

## Goals

- Return a reasonably complete set of pubs in London.
- Estimate the number and cost of Places API requests before running a population job.
- Choose a sensible refresh interval once runtime cost and result quality are understood.

## Research observations

- A single search for `pubs in London` returns only a small subset; the research observed roughly 90 results.
- The working estimate is roughly 3,500 pubs across London, so a single broad search is not an adequate collection strategy.
- The initial estimate was that about half of broad-search results could be duplicates or otherwise poor coverage.
- London was approximated as 40 km by 60 km.
- A uniform grid at roughly 5 km spacing gives about `8 × 12 = 96` cells. The diagonal of a cell is approximately `sqrt(2) × 5 km`, so a search radius based on the cell diagonal would be about 7 km.
- Uniform spacing may undersample central London. Concentric circles or an ellipse, with denser sampling near the centre, are possible follow-up strategies.

## API constraints and cost

- The research found that Places API (New) Nearby Search returns at most 20 results and does not provide a next-page token.
- The legacy Nearby Search was understood to return at most 60 results, so it is not sufficient as a complete London-wide strategy.
- The current code uses text search over each rectangle and follows `nextPageToken` when returned. Its `api_calls` counter currently counts rectangles only; it does not count page-token requests and must not be treated as a billing estimate.
- Historical request and cost estimates are recorded in [`api-cost-research.md`](api-cost-research.md); confirm current Google pricing and page limits before scheduling recurring runs.

## Coordinates recorded during research

| Point | Coordinates | Approximate location |
| --- | --- | --- |
| Top-left | `(51.670743, -0.497409)` | Near Sarratt |
| Top-right | `(51.667083, 0.264424)` | Near Fox Hatch |
| Bottom-left | `(51.328877, -0.437017)` | Near Cobham |
| Bottom-right | `(51.373541, 0.277825)` | Near Fawkham |
| Centre | `(51.509408, -0.132653)` | Fallow |

The research also notes that the Ordnance Survey National Grid / British National Grid is a possible coordinate system for future spatial modelling, but the current utility uses latitude/longitude directly.

## Follow-up measurements

Before changing the grid strategy, record for each cell:

- requests made, including every page-token request;
- results returned and unique results retained;
- duplicate rate across neighbouring cells;
- whether the API result limit was reached;
- runtime and estimated cost.

These measurements will determine whether a denser central grid, concentric rings, or an ellipse is worth the added complexity.
