# MVP algorithm plan

The [algorithm research](research.md) holds the assumptions, cost baseline, and background to the methods considered. The [product goals](../product.md#what-makes-a-better-recommendation) define what a better recommendation means. This plan records the current approach and may change as we test it.

## Initial baseline

For the MVP, we need a simple algorithm that can suggest pubs quickly. This gives us a clear target for getting the product into users' hands, while leaving room to explore new ideas and improve the recommendations during development.

Given the group's starting locations and a requested number of venues, calculate their geographic centre and select that many nearby pubs or bars. For the MVP, start with three options so the group has a choice. Calculate each participant's journey to each venue using their selected transport mode, then rank the venues by total group journey time. This gives the group travel times to compare. Because the shortlist is based on geographic distance, it could miss better meeting points on London's transport network.

## Experiments

Explore other approaches during MVP development:

- Narrow the candidate pubs before checking journeys, for example by considering only pubs within a bounding box around the group's locations, or randomly sampling a small number with a bias towards preset transfer hubs. We could then compare actual journeys to the shortlisted pubs.
- Try simulated annealing. It may give a better answer than the geographic centre with fewer API calls than brute force, though it could still be too costly as a long-term solution.
- Use precomputed travel-time graphs, potentially for different times of day and transport modes, to shortlist pubs. Then use live routing information to choose among them.
- For demos, consider a precomputed set of recommended pubs to show the product vision.

## Deferred methods

- Brute force is too costly for routine searches: routing alone can cost tens of dollars or more per search for a group of four. See the [cost baseline](research.md#brute-force-cost-baseline). It could later serve as a benchmark for tests or monitoring.
- Bayesian inference would take more work to develop. We will revisit it when Tim Viney is available to work on the approach.

## Testing and evaluation

Use a strategy pattern to make it easy to switch between and compare methods.

Set up repeatable scenarios that serve as unit tests for each search method and as evaluation cases for comparing their suggestions. Use the unit tests to catch changes in behaviour. For evaluation, measure total journey time first, then how evenly journey times are shared across the group. Also record routing calls and response time so we can judge the cost of an improvement. Where a scenario has a known best option under these measures, compare each method's result with it.
