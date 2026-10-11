# API Cost Research

This document records the API-provider comparison used when assessing the cost of populating the London pubs dataset. The figures are historical research notes and must be checked against current provider documentation before implementation or scheduling.

## Initial direction

Google Maps was the first provider to investigate. The goal was to identify the largest useful free allowance and then compare the cheapest practical paid option.

## Provider comparison

| Provider | API | Research notes | Free allowance | Cost per 1,000 |
| --- | --- | --- | ---: | ---: |
| Google Maps | Places (New) | Additional fields such as ratings may increase the cost | — | 32 |
| Google Maps | Routes — live routing | — | — | 10 |
| Google Maps | Routes — basic | — | — | 5 |
| Mapbox | Directions API | — | 100,000 | 2 |
| Mapbox | Places | Bounding-box search may be possible | 25,000 | 1.70 |
| TravelTime | — | Subscription pricing requires contacting the provider | — | — |

## Research notes

- Google’s former `$200` general credit was expected to move toward per-API quotas from 1 March. Confirm the effective date and current billing model.
- Google Maps sessions are not expected to reduce the cost of this batch-population workflow.
- Confirm the currency, billing unit, current free quotas, and field-level pricing against provider documentation.
- For the London population job, cost must be calculated from actual requests, including every page-token request, rather than from the number of grid cells alone.

## Relationship to pub population

The current pub population strategy uses Google Places Text Search over a grid of London rectangles. Its historical estimate was approximately 100 searches across up to 10 pages, or around 1,000 requests and roughly 30 in provider billing. This is an estimate only; request counts and current pricing must be measured and verified before recurring runs are enabled.
