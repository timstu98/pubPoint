# Suggest Pub Decision Document

## Summary

### Challenge

Api calls turned out to be more expensive (monetarily) than first conceived. Minimising api calls for a user search will be key. This will require as much pre-compute as possible to minimise cost. The brute-force approach cost for one group search is estimated below, and acts as a baseline to compare other strategies against.

### Solution

We will develop a general purpose algorithm and a specific 2-person group algorithm. The 2 person algorithm can be seperate as due to two users, its important for the user to feel a rapid response time and know a sensible pub has been suggested, or else trust in the service will decrease. Also there only being two people makes it cheap to do.

The first iteration of the general propose algorithm will userBayesian Inference. It is the only option that will provide a good solution not stuck in local minima while having the potential to have mostly pre-compute and little real time api usage.

The 2-person solution will be developed in stages. Stage:

1. Suggest the pub in the middle of the two people.
2. Use simulated annealing to pick a suitable pub. Hope is this will require a sufficiently small number of iterations and therefore real time API calls.

## Problem and Assumptions Definition

The aim of this app is to suggest pubs to groups of users based on their chosen location. Initially, I will reduce the solution space for simplicity of development and to allow comparison between methods and algorithms.

First, we will only be looking at pubs in London. ChatGPT suggests there are approximately 3,500 pubs in London. Ultimately, I would like to extend the functionality to other cities and areas, and consider venues beyond just pubs.

In theory, groups could be of any size. For algorithm comparison, I will assume a size of 4, which is non-trivial and likely representative of the future average group size.

Ultimately, I would like to fine-tune the algorithm to prioritize different characteristics of pubs (e.g., quality of food), filter the pubs (e.g., closing times, dog-friendly), and compute different modes of transport for the users. These add significant complexity to the algorithm, so most of these features will be included down the line.

### Brute Force Approach Baseline

This is a brute force approach to finding the best bar/pub in London that guarantees an optimal solution. Every other strategy can be considered an improvement upon this cost estimate and can be evaluated relative to this approach.

Checking every venue for every person requires `3,500 venues × 4 people = 14,000` journeys for one group search, using one transport mode. The estimate below applies the first paid pricing tier to all 14,000 journeys, with no free allowance. It covers journey-time calculations only, not collecting venue data.

| Provider and API                   |              Paid rate | Cost for one group search |
| ---------------------------------- | ---------------------: | ------------------------: |
| Google Routes, basic (Essentials)  |  $5 per 1,000 journeys |                       $70 |
| Google Routes, traffic-aware (Pro) | $10 per 1,000 journeys |                      $140 |
| Mapbox Directions or Matrix        |  $2 per 1,000 journeys |                       $28 |

For Google Compute Route Matrix and Mapbox Matrix, a journey is a billable origin-destination element. Batching elements into fewer API requests does not reduce this estimate. TravelTime has fixed annual commercial licence pricing, so it cannot be assigned a per-search price from its public rates. The routing provider and transport mode have not been selected; these figures are comparison estimates, not a forecast of the eventual bill. See [API cost research](../development/api-cost-research.md) for provider pricing.

## Options considered

The detailed algorithm comparison, maths notation, and simulated annealing notes are recorded in [`../algorithms/suggest-pub-algorithms.md`](../algorithms/suggest-pub-algorithms.md).
