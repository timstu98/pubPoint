# Suggest Pub Algorithms

## Options considered

Maths notation:

- `N_u` - Number of users in group
- `N_p` - Number of pubs in London
- `c_sj` - cost of a simple api journey call

### Brute Force

This is clearly too costly.

### Gradient Descent and Similar Methods

Gradient descent is only a local optimization algorithm, so it will not be suitable for our potentially complex solution space, which likely has many local minima.

### Simulated Annealing

Simulated Annealing (SA) is a probabilistic optimization algorithm inspired by the annealing process in metallurgy. It starts with a high "temperature," allowing the algorithm to explore the solution space broadly, accepting worse solutions with some probability to escape local minima. As the temperature decreases over iterations, the search becomes more refined, converging towards an optimal or near-optimal solution.

Why it might be applicable to this problem:

- The problem space is large (~3,500 pubs), making exhaustive search infeasible.
- The function to optimize (total journey time) is likely non-convex, with many local minima.
- SA helps avoid getting stuck in local minima by probabilistically exploring suboptimal solutions early on.
- It can work with constraints (e.g., filtering pubs based on closing time or rating) by modifying the acceptance criteria.

Potential downsides:

- It may require fine-tuning of the cooling schedule to balance exploration and convergence.
- It does not guarantee finding the absolute best solution but provides a good approximation.

The major issue is that, while it’s difficult to give an exact number, the number of real time “live” api calls is likely to sitll be in the dozens (say 100?) which would COST THIS MUCH.

### Bayesian Inference

Bayesian Inference is a probabilistic approach that updates beliefs about a solution iteratively based on new data. It can be used in this context to model uncertainty and improve pub selection dynamically.

Why it might be applicable to this problem:

- It allows incorporating prior knowledge, such as historical user preferences or typical travel patterns.
- The algorithm can dynamically update based on real-time data (e.g., live transport conditions, user feedback on selected pubs).
- It is well-suited for adaptive recommendation systems, where the model continuously improves as more data is collected.

Potential downsides:

- Requires good prior models and sufficient data to converge to useful insights.
- Computationally more expensive than heuristics like simulated annealing or greedy algorithms.

Bayesian inference could be particularly useful when the project expands to personalizing pub recommendations based on user preferences (e.g., weighting quality of food more heavily for some users).

This includes prior knowledge, and prior knowledge is relatively cheap. This is why this method is preferred.

### 2-Person Scenario

We will have the potential to get caught in local minima.

- Gradient Descent is likely to get trapped in the many local minima.
- Simulated Annealing is well-suited for problems with many local minima as it probabilistically explores the solution space.

### Additional Notes on Simulated Annealing

The concept of annealing comes from metallurgy, where heating a metal to a high temperature and then allowing it to cool strengthens the material by removing impurities.

In optimization, the "heating" phase makes the algorithm more willing to accept worse solutions early in the search process. This is controlled via a temperature parameter. As the temperature decreases, the algorithm becomes less likely to accept worse solutions, thereby refining the solution towards an optimal state.
