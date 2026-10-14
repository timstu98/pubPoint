# Pub recommendation algorithm research

This document holds the assumptions, cost baseline, and background for approaches considered for suggesting a pub. The [MVP plan](mvp.md) records the current approach and implementation order.

## Problem and assumptions

The app suggests a pub for a group from its members' starting locations. For comparison, consider only pubs in London, one transport mode per person, and a group of four. The assumed 3,500 London pubs are an approximate planning figure, not a verified count. Groups of other sizes, other cities and venues, venue characteristics, and multiple transport modes may be considered later.

Notation used below:

- `N_u`: number of people in the group
- `N_p`: number of candidate pubs
- `c_sj`: cost of one simple journey calculation

## Brute-force cost baseline

Checking every venue for every person gives `N_p × N_u` journeys. With 3,500 pubs and four people, that is 14,000 journeys for one group search using one transport mode. The estimate applies the first paid pricing tier to all journeys, with no free allowance. It covers journey-time calculations only, not venue data collection.

| Provider and API                   |              Paid rate | Cost for one group search |
| ---------------------------------- | ---------------------: | ------------------------: |
| Google Routes, basic (Essentials)  |  $5 per 1,000 journeys |                       $70 |
| Google Routes, traffic-aware (Pro) | $10 per 1,000 journeys |                      $140 |
| Mapbox Directions or Matrix        |  $2 per 1,000 journeys |                       $28 |

For Google Compute Route Matrix and Mapbox Matrix, each origin-destination result is billable. Batching results into fewer requests does not reduce this estimate. TravelTime uses fixed annual commercial licence pricing, so its public rates do not yield a per-search cost. The provider and transport mode have not been selected; these figures are comparison estimates. See [API cost research](../development/api-cost-research.md) for provider pricing and the [business case](../business-case.md) for costs at smaller candidate counts.

## Methods considered

### Brute force

Calculate each person's journey to every candidate pub and compare the results. This provides a baseline for evaluating other approaches, but the 14,000-journey estimate makes it too expensive for a routine search at the assumed scale.

### Geographic centre

Find the geographic centre of the group's starting locations and suggest a pub there. This is a simple starting point, but the centre of coordinates may not be the fairest meeting point when journeys follow London's transport network. This goes against the key idea and use case of this product.

### Narrow the candidate pubs

Reduce the number of pubs before requesting journey times. One option is a bounding box around the group's starting locations, considering only pubs within that area. Another is to sample a small number of pubs at random, with a bias towards preset transfer hubs. We could then request live journeys to the shortlisted pubs and compare them for the group.

A bounding box or small sample limits routing calls, but either may exclude a better pub. The bounding box and sampling rules would need testing against known scenarios.

### Gradient descent and related local methods

Move through nearby candidate solutions in the direction of an improvement. Journey-time results across pubs may have many local minima, so a local method could settle on a poor candidate.

### Simulated annealing

Simulated annealing explores candidate pubs while its "temperature" is high, sometimes accepting a worse result to escape a local minimum. As the temperature falls, the search becomes more selective. A possible implementation would score candidates using group journey times, adjust the acceptance probability over successive iterations, and apply venue constraints in the score or candidate set.

It can work across a large, irregular search space and with constraints such as closing times or ratings. It needs a cooling schedule and does not guarantee the best pub. The number of live journey calls is uncertain and could still be in the dozens or more, making cost a concern. For two people, it may be worth testing because a quick, sensible suggestion matters to user trust.

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

Alternatively, for very large groups, the best location will actually tend towards the geographic centre of the group, and also the API constraint is higher. We have to make more API calls per suggestion and therefore want to minimise API calls.

This is not likely something we should initially look at, but is a potential improvement down the line.
