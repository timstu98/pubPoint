# MVP algorithm plan

The [algorithm research](research.md) holds the assumptions, cost baseline, and background to the methods considered. This plan records the current approach and may change as we test it.

## MVP approach

For the MVP, we need a simple algorithm that can suggest pubs quickly. This gives us a clear target for getting the product into users' hands, while leaving room to explore new ideas and improve the recommendations during development.

Start with the pub nearest the geographic centre of the group's starting locations. This is quick to implement and gives us a baseline. Geographic distance may be a poor proxy for travel time, especially in London, so we expect to improve on this approach.

We should explore other approaches during MVP development, including:

- Narrow the candidate pubs before checking journeys, for example by considering only pubs within a bounding box around the group's locations, or randomly sampling a small number with a bias towards preset transfer hubs. We could then compare actual journeys to the shortlisted pubs.
- Try simulated annealing. It may give a better answer than the geographic centre with fewer API calls than brute force, though it could still be too costly as a long-term solution.
- Use precomputed travel-time graphs, potentially for different times of day and transport modes, to shortlist pubs. Then use live routing information to choose among them.

Options we are setting aside for the MVP:

- Brute force is too costly for routine searches. Under the lowest rate in our [cost baseline](research.md#brute-force-cost-baseline), checking 3,500 pubs for a group of four costs $28 per search. It could later serve as a benchmark for tests or monitoring.
- Bayesian inference would take more work to develop. We will revisit it when Tim Viney is available to work on the approach.

For demos, we could use a precomputed set of recommended pubs to show the product vision.

## Implementation

Use a strategy pattern to make it easy to switch between and compare methods.

Set up repeatable test scenarios to catch changes in each method's behaviour and compare the quality of its suggestions. Where we know the best pub for a scenario, measure how far each method's result is from it, using total journey time or another metric we choose to optimise.
