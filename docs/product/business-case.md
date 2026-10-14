# Business case

> **Working assumptions** (14 October 2026)

## Routing cost per search

For a group of four, assume one journey-time estimate per person per venue. The estimates below use USD prices at the first paid tier, with no free allowance or volume discount. They cover routing only.

| Venues checked | Journeys | Mapbox Directions or Matrix ($2/1,000) | Google Routes basic ($5/1,000) | Google Routes traffic-aware ($10/1,000) |
| -------------: | -------: | -------------------------------------: | -----------------------------: | --------------------------------------: |
|              1 |        4 |                                 $0.008 |                          $0.02 |                                   $0.04 |
|             10 |       40 |                                  $0.08 |                          $0.20 |                                   $0.40 |
|            100 |      400 |                                  $0.80 |                          $2.00 |                                   $4.00 |
|          3,500 |   14,000 |                                 $28.00 |                         $70.00 |                                 $140.00 |

Finding a suitable venue may require checking several candidates. The 3,500-venue row illustrates a brute-force search, not the intended MVP approach. Mapbox's quoted rate does not cover public transit; the provider and supported transport modes are still to be decided.

Rates and other provider constraints are recorded in [API cost research](../development/research/api-cost-research.md). Recheck rates before using these figures for a budget.

## Potential ways to fund searches

Early on, we would need evidence that people actually visit recommended venues to show pubs the value of paying us. At a larger scale, pubs may be willing to pay for access to that audience without proof of each visit. Options to explore include:

- Pubs paying to sponsor placement in search results.
- Pubs offering discounts that users show or redeem at the bar, which could also help demonstrate visits.
- Pubs paying to be listed on the service, similar to a comparison site, though this may be a poor fit.
- General sponsorship or advertising.
- Commission on restaurant, bar, or pub bookings made through the app.

As usage grows, we could also reduce routing costs by negotiating better API rates, including with Mapbox, or eventually building our own routing infrastructure. These are possibilities to test, not assumed savings.
