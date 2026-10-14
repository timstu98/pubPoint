# API Cost Research

This document records the API-provider comparison used when assessing the cost of populating the London pubs dataset. Pricing was checked on 13 October 2026 and must be checked again before implementation or scheduling.

## Initial direction

Google Maps was the first provider to investigate. The goal was to identify the largest useful free allowance and then compare the cheapest practical paid option.

## Provider comparison

Free allowances are monthly. Prices are USD per 1,000 billable requests in the first paid tier, except where noted.

| Provider | API | Research notes | Free allowance | Cost per 1,000 |
| --- | --- | --- | ---: | ---: |
| Google Maps | Places (New), Text Search Pro | Ratings trigger the Enterprise search tier ($35 per 1,000; 1,000 free). | 5,000 | $32 |
| Google Maps | Routes, Compute Routes Pro | Traffic-aware routing triggers this tier. | 5,000 | $10 |
| Google Maps | Routes, Compute Routes Essentials | Basic routing. | 10,000 | $5 |
| Mapbox | Directions API | Billed per route request. | 100,000 | $2 |
| Mapbox | Search Box API, category requests | Supports bounding-box filtering. Results are for temporary use; storing them requires an arrangement with Mapbox. Standard pricing shown. | 25,000 | $1.70 |
| TravelTime | Routes, Matrix, Isochrone | Free access is for testing and integration. Commercial licences have fixed annual pricing rather than per-request charges. | No monthly quota published; free keys limited to 120 hits/min | — |

## Research notes

- Google Maps sessions are not expected to reduce the cost of this batch-population workflow.
- Google Maps now publishes free monthly usage caps by SKU, rather than a general `$200` credit. The requested Places fields determine the billed SKU.
- Mapbox Search Box category requests are priced per request. Its temporary-use restriction may rule it out for building a persistent pubs dataset without a separate agreement.
- For the London population job, cost must be calculated from actual requests, including every page-token request, rather than from the number of grid cells alone.

Sources: [Google pricing](https://developers.google.com/maps/billing-and-pricing/pricing), [Google route billing](https://developers.google.com/maps/documentation/routes/usage-and-billing), [Google Places fields](https://developers.google.com/maps/documentation/places/web-service/data-fields), [Mapbox pricing](https://www.mapbox.com/pricing), [Mapbox Search Box documentation](https://docs.mapbox.com/api/search/search-box/), [Mapbox Directions documentation](https://docs.mapbox.com/api/navigation/directions/), [TravelTime usage limits](https://docs.traveltime.com/api/overview/usage-limits), [TravelTime licence options](https://help.traveltime.com/en/articles/9685030-licence-options).

## Relationship to pub population

The current pub population strategy uses Google Places Text Search over a grid of London rectangles. Its historical estimate was approximately 100 searches across up to 10 pages, or around 1,000 requests. At the current Text Search Pro rate, that would be about $32 before the monthly free allowance, and $0 if all requests fall within the 5,000 free Pro requests. This is an estimate only; actual request counts, selected fields, other usage of the same SKU, and current pricing must be measured and verified before recurring runs are enabled.
