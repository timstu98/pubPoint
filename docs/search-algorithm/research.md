# Pub recommendation algorithm research

This document holds the assumptions, cost baseline, and background for approaches considered for suggesting a venue. The [product goals](../product/vision.md#what-makes-a-better-recommendation) define recommendation quality; the [MVP plan](mvp.md) records the current approach.

## Problem

Finding a good pub or bar for a group may require comparing journeys to many venues. Calculating every person's journey to every pub would identify the best option under a chosen scoring method, but the routing cost is too high for routine use.

The brute-force calculation below estimates the cost of checking every candidate using an indicative set of assumptions. It provides a baseline for methods that evaluate fewer pubs.

## Brute-force cost baseline

For this estimate, assume London only, approximately 3,500 pubs, and a group of four. The pub count is a planning figure, not a verified total. Each participant has one selected transport mode, though participants may choose different modes. Other group sizes, cities, venues, venue characteristics, and multiple modes for one participant are outside this calculation.

Notation used below:

- `N_u`: number of people in the group
- `N_p`: number of candidate pubs

Checking every venue for every person gives `N_p × N_u` journeys. With 3,500 pubs and four people, that is 14,000 journeys for one group search, with one selected transport mode per participant. The estimate applies the first paid pricing tier to all journeys, with no free allowance. It covers journey-time calculations only, not venue data collection.

| Provider and API                   |              Paid rate | Cost for one group search |
| ---------------------------------- | ---------------------: | ------------------------: |
| Google Routes, basic (Essentials)  |  $5 per 1,000 journeys |                       $70 |
| Google Routes, traffic-aware (Pro) | $10 per 1,000 journeys |                      $140 |
| Mapbox Directions or Matrix        |  $2 per 1,000 journeys |                       $28 |

For Google Compute Route Matrix and Mapbox Matrix, each origin-destination result is billable. Batching results into fewer requests does not reduce this estimate. TravelTime uses fixed annual commercial licence pricing, so its public rates do not yield a per-search cost. The provider and transport modes have not been selected; these figures are comparison estimates. Mapbox [Directions](https://docs.mapbox.com/api/navigation/directions/) and [Matrix](https://docs.mapbox.com/api/navigation/matrix/) support driving, walking, and cycling, but not public transit, so their rate does not cover every transport choice the product may need. See [API cost research](../development/research/api-cost-research.md) for provider pricing.

## Methods considered

### Brute force

Calculate each person's journey to every candidate pub and compare the results. This provides a baseline for evaluating other approaches, but the 14,000-journey estimate makes it too expensive for a routine search at the assumed scale.

### Geographic centre

Find the geographic centre of the group's starting locations and return the requested number of pubs or bars nearest to it. This gives us a quick baseline, but the centre could make a poor meeting point on the transport network, diminishing the main aim of the product.

### Narrow the candidate pubs

Reduce the number of pubs before requesting journey times. One option is a bounding box around the group's starting locations, considering only pubs within that area. Another is to sample a small number of pubs at random, with a bias towards preset transfer hubs. We could then request live journeys to the shortlisted pubs and compare them for the group.

A bounding box or small sample limits routing calls, but either may exclude a better pub. The bounding box and sampling rules would need testing against known scenarios.

### Gradient descent and related local methods

Move through nearby candidate solutions in the direction of an improvement. Journey-time results across pubs may have many local minima, so a local method could settle on a poor candidate.

### Simulated annealing

Simulated annealing explores candidate pubs while its "temperature" is high, sometimes accepting a worse result to escape a local minimum. As the temperature falls, the search becomes more selective. A possible implementation would score candidates using group journey times, adjust the acceptance probability over successive iterations, and apply venue constraints in the score or candidate set.

It can work across a large, irregular search space and, later, with constraints such as closing times or ratings. These venue criteria are outside the current MVP scope. It needs a cooling schedule and does not guarantee the best pub. The number of live journey calls is uncertain and could still be in the dozens or more, making cost a concern. For two people, it may be worth testing because a quick, sensible suggestion matters to user trust.

### Bayesian inference

A Bayesian approach would start with prior information about likely good meeting points or travel patterns, then update its estimate as it receives journey results or feedback. It could incorporate preferences and adapt recommendations over time. Useful prior information could be precomputed, reducing the need for live calls.

This needs a reliable prior model and enough data to produce useful results. It is more complex to build and tune than a simple heuristic. It may be useful later for personalisation, such as weighting food quality differently for different groups.

### Precomputed travel times with live checks

Represent locations and pubs in a graph of precomputed travel-time estimates, potentially for different times of day and transport modes. Use those estimates to identify promising pubs, then request live routing information for the shortlist before making a recommendation. This could reduce the number of live calls while still checking current conditions for the final candidates. Its usefulness depends on how well the stored estimates represent the group's actual journeys.

### Precomputed demo suggestions

For a demonstration, prepare a fixed set of recommended pubs in advance to show the intended experience. This would illustrate the product vision without evaluating a general recommendation method for each new group.

## Varying strategies based upon group size

We may have slightly different requirements and constraints for different group sizes, and therefore may want to vary strategy based upon the group size.

For a group of two, it's very easy for the user to see whether the suggestion is accurate, as they will have a good idea of what the best pub would be for them. Therefore, it's incredibly important to be accurate for this when suggesting a pub, and API calls are less of a constraint.

For very large groups, a centre-based suggestion might become more useful, but each additional person also increases the number of journeys to check. This may favour methods that limit routing calls.

This is not likely something we should initially look at, but is a potential improvement down the line.
